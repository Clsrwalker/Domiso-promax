#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
from collections import deque
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import domiso_pipeline_literal as base
import midi_to_domiso_dense3layer as core


PLAYABLE_NOTES = {
    60, 62, 64, 65, 67,
    69, 71, 72, 74, 76,
    77, 79, 81, 83, 84,
}
PLAYABLE_MIN = min(PLAYABLE_NOTES)
PLAYABLE_MAX = max(PLAYABLE_NOTES)
LOW_ROW_MAX = 67
MID_ROW_MIN = 69
MID_ROW_MAX = 76
HIGH_ROW_MIN = 77
LEAD_FOCUS_MIN = 69
LEAD_FOCUS_MAX = 81
SKY_LAYOUT = "Y U I O P / H J K L ; / N M , . /"
BASE_OFFSETS = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
SKY_SUPPORT_MIN_GAP_MS = 92.0
SKY_SUPPORT_SAME_KEY_MS = 118.0
SKY_LEAD_MIN_GAP_MS = 84.0
SKY_LEAD_SAME_KEY_MS = 108.0
SKY_BURST_GAP_MS = 92.0
SKY_MAX_CLUSTERS_PER_SEC = 9
SKY_MAX_LEAD_CLUSTERS_PER_SEC = 11


@dataclass(frozen=True)
class Profile:
    name: str
    desc: str
    shift_min: int
    shift_max: int
    shift_bias: float
    dynamic: bool
    dynamic_offsets: Tuple[int, ...]
    max_changes: int
    b_max_poly: int
    c_max_poly: int


PROFILES: Dict[str, Profile] = {
    "sky_literal": Profile(
        "sky_literal",
        "Sky 15-key literal-balance: preserve more source body than melodylock, but trim mid clutter to fit C4-C6",
        -12,
        12,
        0.28,
        True,
        (0, -2, -1, 1, 2),
        1,
        6,
        2,
    ),
    "sky_literal_dense": Profile(
        "sky_literal_dense",
        "Sky 15-key literal-balance dense: keep more inner rhythm/body while still preventing mush",
        -12,
        12,
        0.22,
        True,
        (0, -3, -2, -1, 1, 2),
        2,
        8,
        2,
    ),
}


def analyze_midi(parsed: dict) -> dict:
    notes = parsed["notes"]
    tpb = parsed["tpb"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    duration = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    events = []
    for n in notes:
        events.append((n["start"], 1))
        events.append((n["end"], -1))
    events.sort()
    poly, max_poly = 0, 0
    for _, d in events:
        poly += d
        max_poly = max(max_poly, poly)
    ts = parsed["time_sigs"][0] if parsed["time_sigs"] else (0, 4, 4)
    bar_ticks = int(max(1, tpb * ts[1] * (4 / ts[2])))
    by_bar = Counter(n["start"] // bar_ticks for n in notes)
    bars = [by_bar[i] for i in range(max(by_bar) + 1)] if by_bar else [0]
    p90 = statistics.quantiles(bars, n=10)[8] if len(bars) >= 10 else max(bars)
    return {
        "note_count": len(notes),
        "duration_s": duration,
        "tempo0": tempos[0][1],
        "tempo_events": len(tempos),
        "time_sig": f"{ts[1]}/{ts[2]}",
        "max_poly": max_poly,
        "bar_density_mean": float(statistics.mean(bars)),
        "bar_density_p90": float(p90),
        "tracks": len(parsed["track_medians"]),
        "pitch_min": min(n["note"] for n in notes),
        "pitch_max": max(n["note"] for n in notes),
    }


def recommend_profile(metrics: dict) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if metrics["max_poly"] >= 6 or metrics["bar_density_p90"] >= 16:
        reasons.append("15-key range + dense source -> sky_literal_dense")
        return "sky_literal_dense", reasons
    reasons.append("default Sky literal-balance profile")
    return "sky_literal", reasons


def fold_and_snap_sky(pitch: int) -> Tuple[int, float]:
    folded = pitch
    while folded < PLAYABLE_MIN:
        folded += 12
    while folded > PLAYABLE_MAX:
        folded -= 12
    best = min(
        PLAYABLE_NOTES,
        key=lambda p: (abs(p - folded), abs(p - pitch), abs(p - 72), p),
    )
    return best, abs(best - folded)


def evaluate_shift_cost_sky(notes: List[dict], shift: int, top_ids: Set[int], melody_track: int, tpb: int) -> float:
    total = 0.0
    short_limit = max(1, tpb // 6)
    for idx, note in enumerate(notes):
        mapped, dist = fold_and_snap_sky(note["note"] + shift)
        dur = note["end"] - note["start"]
        weight = 1.0
        if idx in top_ids:
            weight += 1.0
        if note["track"] == melody_track:
            weight += 0.55
        if dur <= short_limit:
            weight *= 0.75
        total += dist * weight

        lead_like = idx in top_ids or note["track"] == melody_track
        if lead_like:
            if mapped < LEAD_FOCUS_MIN:
                total += (LEAD_FOCUS_MIN - mapped) * 0.22
            elif mapped > LEAD_FOCUS_MAX:
                total += (mapped - LEAD_FOCUS_MAX) * 0.18
        elif mapped < PLAYABLE_MIN + 1 or mapped > PLAYABLE_MAX - 1:
            total += 0.08
    return total


def choose_base_shift_profile(
    notes: List[dict], top_ids: set, melody_track: int, tpb: int, p: Profile
) -> int:
    best_s, best_c = 0, float("inf")
    for s in range(p.shift_min, p.shift_max + 1):
        c = evaluate_shift_cost_sky(notes, s, top_ids, melody_track, tpb) + p.shift_bias * abs(s)
        if c < best_c:
            best_s, best_c = s, c
    return best_s


def choose_dynamic_shifts_profile(
    notes: List[dict], top_ids: set, melody_track: int, tpb: int, base_shift: int, p: Profile
) -> Tuple[List[int], int, int]:
    win_ticks = max(1, tpb * 16)
    max_win = max(n["start"] // win_ticks for n in notes)
    cnt = max_win + 1
    if not p.dynamic:
        return [base_shift] * cnt, win_ticks, 0

    cands = sorted(
        {base_shift + d for d in p.dynamic_offsets if p.shift_min <= base_shift + d <= p.shift_max}
        | {base_shift}
    )
    by_w = defaultdict(list)
    for i, n in enumerate(notes):
        by_w[n["start"] // win_ticks].append((i, n))

    local_costs = []
    for w in range(cnt):
        entries = by_w.get(w, [])
        vals = {}
        for shift in cands:
            total = 0.0
            for gi, n in entries:
                mapped, dist = fold_and_snap_sky(n["note"] + shift)
                weight = 1.0
                if gi in top_ids:
                    weight += 1.0
                if n["track"] == melody_track:
                    weight += 0.55
                total += dist * weight
                if gi in top_ids or n["track"] == melody_track:
                    if mapped < LEAD_FOCUS_MIN:
                        total += (LEAD_FOCUS_MIN - mapped) * 0.22
                    elif mapped > LEAD_FOCUS_MAX:
                        total += (mapped - LEAD_FOCUS_MAX) * 0.18
            vals[shift] = total
        local_costs.append(vals)

    dp = {(shift, 0): local_costs[0][shift] for shift in cands}
    back = [{(shift, 0): None for shift in cands}]
    for w in range(1, cnt):
        ndp = {}
        nb = {}
        for shift in cands:
            for (prev_shift, changes), prev_cost in dp.items():
                next_changes = changes + (1 if shift != prev_shift else 0)
                if next_changes > p.max_changes:
                    continue
                cost = prev_cost + local_costs[w][shift]
                if shift != prev_shift:
                    cost += 2.6 + 0.26 * abs(shift - prev_shift)
                key = (shift, next_changes)
                if key not in ndp or cost < ndp[key]:
                    ndp[key] = cost
                    nb[key] = (prev_shift, changes)
        if not ndp:
            ndp = {(base_shift, 0): min(dp.values())}
            nb = {(base_shift, 0): min(dp, key=lambda k: dp[k])}
        dp = ndp
        back.append(nb)

    state = min(dp, key=lambda k: dp[k])
    shifts = [base_shift] * cnt
    for w in range(cnt - 1, -1, -1):
        shifts[w] = state[0]
        prev = back[w].get(state)
        if prev is None:
            break
        state = prev
    changes = sum(1 for i in range(1, len(shifts)) if shifts[i] != shifts[i - 1])
    return shifts, win_ticks, changes


def map_notes_sky(notes: List[dict], shifts: List[int], win_ticks: int, tick_per_step: float) -> Tuple[List[dict], float]:
    mapped = []
    total_dist = 0.0
    for n in notes:
        win = min(len(shifts) - 1, max(0, n["start"] // win_ticks))
        shift = shifts[win]
        pitch, dist = fold_and_snap_sky(n["note"] + shift)
        start_step = int(round(n["start"] / tick_per_step))
        end_step = int(round(n["end"] / tick_per_step))
        if end_step <= start_step:
            end_step = start_step + 1
        total_dist += dist
        mapped.append(
            {
                "start_step": start_step,
                "end_step": end_step,
                "dur_steps": end_step - start_step,
                "pitch": pitch,
                "track": n["track"],
                "vel": n["vel"],
            }
        )
    return mapped, total_dist


def annotate_mapped_notes(
    notes: List[dict], mapped_notes: List[dict], top_ids: Set[int], melody_track: int
) -> List[dict]:
    out = []
    for idx, (src, mapped) in enumerate(zip(notes, mapped_notes)):
        row = dict(mapped)
        row["src_idx"] = idx
        row["src_note"] = src["note"]
        row["is_top"] = idx in top_ids
        row["is_melody_track"] = src["track"] == melody_track
        out.append(row)
    return out


def score_lead_note(
    note: dict, prev_pitch: Optional[int], prev_end: int, step: int, melody_track: int
) -> float:
    score = 0.0
    if note["track"] == melody_track:
        score += 6.0
    if note["is_top"]:
        score += 2.2
    score += min(1.8, 0.35 * note["dur_steps"])
    score += min(1.2, note["vel"] / 96.0)
    if step % 4 == 0:
        score += 0.35
    if LEAD_FOCUS_MIN <= note["pitch"] <= LEAD_FOCUS_MAX:
        score += 0.65
    elif MID_ROW_MIN <= note["pitch"] <= HIGH_ROW_MIN:
        score += 0.25
    elif note["pitch"] < LOW_ROW_MAX:
        score -= min(2.0, (LOW_ROW_MAX - note["pitch"]) * 0.16)
    elif note["pitch"] > PLAYABLE_MAX - 1:
        score -= min(1.5, (note["pitch"] - (PLAYABLE_MAX - 1)) * 0.16)

    if prev_pitch is not None:
        leap = abs(note["pitch"] - prev_pitch)
        if leap <= 2:
            score += 0.9
        elif leap <= 5:
            score += 0.7
        elif leap <= 9:
            score += 0.2
        elif leap >= 17:
            score -= 2.0
        elif leap >= 12:
            score -= 1.0
        if step < prev_end and note["track"] != melody_track:
            score -= 0.8
        if note["pitch"] == prev_pitch and step <= prev_end:
            score -= 0.4
    return score


def pick_lead_candidate(
    candidates: List[dict], prev_pitch: Optional[int], prev_end: int, step: int, melody_track: int
) -> Optional[dict]:
    melody_candidates = [n for n in candidates if n["track"] == melody_track]
    if melody_candidates:
        pool = melody_candidates
    else:
        if step < prev_end:
            return None
        pool = [n for n in candidates if n["is_top"] or n["dur_steps"] >= 2 or n["vel"] >= 80]
        if not pool:
            return None
        if step % 4 != 0 and max(n["dur_steps"] for n in pool) <= 1:
            return None

    scored = []
    for n in pool:
        scored.append((score_lead_note(n, prev_pitch, prev_end, step, melody_track), n))
    scored.sort(
        key=lambda x: (
            x[0],
            x[1]["track"] == melody_track,
            x[1]["is_top"],
            x[1]["dur_steps"],
            x[1]["pitch"],
        ),
        reverse=True,
    )
    return scored[0][1]


def extract_melody_intervals(mapped_notes: List[dict], melody_track: int) -> Tuple[List[Tuple[int, int, int]], Set[int], dict]:
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)

    lead: List[Tuple[int, int, int, int]] = []
    selected_ids: Set[int] = set()
    stats = {
        "lead_notes": 0,
        "lead_from_melody_track": 0,
        "lead_from_top_note": 0,
        "fallback_lead_notes": 0,
    }

    prev_pitch: Optional[int] = None
    prev_end = -1
    for step in sorted(by_start):
        cand = pick_lead_candidate(by_start[step], prev_pitch, prev_end, step, melody_track)
        if cand is None:
            continue

        start = step
        end = max(start + 1, cand["end_step"])
        if lead:
            last_start, last_end, last_pitch, last_idx = lead[-1]
            if start < last_end:
                if start <= last_start:
                    lead.pop()
                else:
                    lead[-1] = (last_start, start, last_pitch, last_idx)

        if lead and lead[-1][2] == cand["pitch"] and start <= lead[-1][1] + 1:
            last_start, last_end, last_pitch, last_idx = lead[-1]
            lead[-1] = (last_start, max(last_end, end), last_pitch, last_idx)
        else:
            lead.append((start, end, cand["pitch"], cand["src_idx"]))

        selected_ids.add(cand["src_idx"])
        stats["lead_notes"] += 1
        if cand["track"] == melody_track:
            stats["lead_from_melody_track"] += 1
        else:
            stats["fallback_lead_notes"] += 1
        if cand["is_top"]:
            stats["lead_from_top_note"] += 1

        prev_pitch = cand["pitch"]
        prev_end = end

    intervals = [(s, e, p) for s, e, p, _ in lead if e > s]
    return base.merge_intervals_strict(intervals), selected_ids, stats


def build_active_pitch_map(intervals: List[Tuple[int, int, int]], total_steps: int) -> List[Optional[int]]:
    active: List[Optional[int]] = [None] * total_steps
    for start, end, pitch in intervals:
        for step in range(max(0, start), min(total_steps, end)):
            active[step] = pitch
    return active


def build_step_ms(total_steps: int, tempo_steps: List[Tuple[int, int]]) -> List[float]:
    ms = [0.0] * (total_steps + 1)
    if total_steps <= 0:
        return ms
    tempo_idx = 0
    current_bpm = tempo_steps[0][1] if tempo_steps else 120
    for step in range(total_steps):
        while tempo_idx + 1 < len(tempo_steps) and tempo_steps[tempo_idx + 1][0] <= step:
            tempo_idx += 1
            current_bpm = tempo_steps[tempo_idx][1]
        ms[step + 1] = ms[step] + (60000.0 / current_bpm / 4.0)
    return ms


def prune_lead_for_input_speed(
    intervals: List[Tuple[int, int, int]], step_ms: List[float]
) -> Tuple[List[Tuple[int, int, int]], int]:
    arr = sorted(intervals, key=lambda x: (x[0], x[1], x[2]))
    if not arr:
        return [], 0

    out: List[Tuple[int, int, int]] = []
    pruned = 0
    burst_keep_toggle = False
    prev_gap_ms = float("inf")

    for i, (s, e, p) in enumerate(arr):
        if e <= s:
            continue
        d = e - s
        strong = (s % 4) == 0
        eighth = (s % 2) == 0
        prev_pitch = out[-1][2] if out else None
        next_pitch = arr[i + 1][2] if i + 1 < len(arr) else None

        if out:
            gap_ms = step_ms[s] - step_ms[out[-1][0]]
            if p == out[-1][2] and gap_ms < SKY_LEAD_SAME_KEY_MS:
                out[-1] = (out[-1][0], max(out[-1][1], e), out[-1][2])
                pruned += 1
                prev_gap_ms = gap_ms
                continue
        else:
            gap_ms = float("inf")

        if gap_ms >= SKY_BURST_GAP_MS:
            burst_keep_toggle = False

        contour_peak = (
            prev_pitch is not None
            and next_pitch is not None
            and ((p > prev_pitch and p > next_pitch) or (p < prev_pitch and p < next_pitch))
        )

        if out and gap_ms < SKY_LEAD_MIN_GAP_MS and d <= 2 and not strong:
            should_drop = False
            if not contour_peak and not eighth:
                should_drop = True
            elif prev_gap_ms < SKY_BURST_GAP_MS:
                burst_keep_toggle = not burst_keep_toggle
                should_drop = burst_keep_toggle
            if should_drop:
                pruned += 1
                prev_gap_ms = gap_ms
                continue

        if out and gap_ms < 70.0 and not strong and d <= 1:
            pruned += 1
            prev_gap_ms = gap_ms
            continue

        out.append((s, e, p))
        prev_gap_ms = gap_ms

    return base.merge_intervals_strict(out), pruned


def apply_input_budget_constraints(
    voices: Dict[str, List[Tuple[int, int, int]]],
    step_ms: List[float],
) -> Tuple[Dict[str, List[Tuple[int, int, int]]], int]:
    events = []
    for voice in ("A", "C", "B"):
        for idx, (s, e, pitch) in enumerate(voices[voice]):
            if e > s:
                events.append({"voice": voice, "idx": idx, "s": s, "e": e, "pitch": pitch})

    def event_rank(ev: dict) -> Tuple[int, int, int]:
        strong = 0 if (ev["s"] % 4) == 0 else 1
        voice_rank = {"A": 0, "C": 1, "B": 2}[ev["voice"]]
        return (ev["s"], strong, voice_rank)

    events.sort(key=event_rank)
    recent_clusters: deque[float] = deque()
    last_cluster_step: Optional[int] = None
    last_cluster_time = float("-inf")
    last_pitch_time: Dict[int, float] = {}
    last_pitch_event: Dict[int, dict] = {}
    kept: Dict[str, List[dict]] = {"A": [], "B": [], "C": []}
    dropped = 0

    for ev in events:
        s = ev["s"]
        t = step_ms[s]
        strong = (s % 4) == 0
        dur_steps = ev["e"] - ev["s"]
        same_step = last_cluster_step == s

        while recent_clusters and t - recent_clusters[0] > 1000.0:
            recent_clusters.popleft()

        cluster_gap = float("inf") if same_step or last_cluster_step is None else (t - last_cluster_time)
        same_pitch_gap = t - last_pitch_time.get(ev["pitch"], float("-inf"))

        if ev["voice"] == "A":
            if same_pitch_gap < SKY_LEAD_SAME_KEY_MS:
                ref = last_pitch_event.get(ev["pitch"])
                if ref is not None and ref["voice"] == "A":
                    ref["e"] = max(ref["e"], ev["e"])
                    dropped += 1
                    continue
            if len(recent_clusters) >= SKY_MAX_LEAD_CLUSTERS_PER_SEC and not strong and dur_steps <= 2 and not same_step:
                dropped += 1
                continue
            if cluster_gap < 72.0 and not strong and dur_steps <= 1:
                dropped += 1
                continue
        else:
            if same_pitch_gap < SKY_SUPPORT_SAME_KEY_MS:
                ref = last_pitch_event.get(ev["pitch"])
                if ref is not None and ref["voice"] == ev["voice"]:
                    ref["e"] = max(ref["e"], ev["e"])
                dropped += 1
                continue
            if cluster_gap < SKY_SUPPORT_MIN_GAP_MS and not strong and not same_step:
                dropped += 1
                continue
            if len(recent_clusters) >= SKY_MAX_CLUSTERS_PER_SEC and not strong and not same_step:
                dropped += 1
                continue
            if ev["voice"] == "B" and len(recent_clusters) >= (SKY_MAX_CLUSTERS_PER_SEC - 1) and dur_steps <= 2 and not strong and not same_step:
                dropped += 1
                continue

        record = {"voice": ev["voice"], "s": ev["s"], "e": ev["e"], "pitch": ev["pitch"]}
        kept[ev["voice"]].append(record)
        last_pitch_time[ev["pitch"]] = t
        last_pitch_event[ev["pitch"]] = record
        if not same_step:
            recent_clusters.append(t)
            last_cluster_step = s
            last_cluster_time = t

    out = {
        voice: base.merge_intervals_strict([(ev["s"], ev["e"], ev["pitch"]) for ev in arr])
        for voice, arr in kept.items()
    }
    return out, dropped


def summarize_input_stability(
    voices: Dict[str, List[Tuple[int, int, int]]],
    step_ms: List[float],
) -> Dict[str, float]:
    onset_steps = sorted({s for arr in voices.values() for s, _, _ in arr})
    if not onset_steps:
        return {"clusters_per_sec_peak": 0.0, "min_cluster_gap_ms": 0.0, "same_key_min_gap_ms": 0.0}

    recent: deque[float] = deque()
    peak = 0
    for step in onset_steps:
        t = step_ms[step]
        while recent and t - recent[0] > 1000.0:
            recent.popleft()
        recent.append(t)
        peak = max(peak, len(recent))

    min_cluster_gap = min(
        ((step_ms[onset_steps[i]] - step_ms[onset_steps[i - 1]]) for i in range(1, len(onset_steps))),
        default=0.0,
    )

    per_pitch: Dict[int, List[int]] = defaultdict(list)
    for arr in voices.values():
        for s, _, p in arr:
            per_pitch[p].append(s)
    same_key_gaps = []
    for steps in per_pitch.values():
        steps.sort()
        for i in range(1, len(steps)):
            same_key_gaps.append(step_ms[steps[i]] - step_ms[steps[i - 1]])

    return {
        "clusters_per_sec_peak": float(peak),
        "min_cluster_gap_ms": float(round(min_cluster_gap, 1)),
        "same_key_min_gap_ms": float(round(min(same_key_gaps), 1)) if same_key_gaps else 0.0,
    }


def assign_support_voices(
    mapped_notes: List[dict],
    lead_ids: Set[int],
    lead_pitch_by_step: List[Optional[int]],
    melody_track: int,
    bass_track: int,
) -> Tuple[Dict[str, List[Tuple[int, int, int]]], int]:
    by_start = defaultdict(list)
    for n in mapped_notes:
        if n["src_idx"] in lead_ids:
            continue
        by_start[n["start_step"]].append(n)

    voices = {"B": [], "C": []}
    pruned = 0

    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda x: (x["pitch"], x["track"]))
        strong = (step % 4) == 0
        eighth = (step % 2) == 0
        dense = len(arr) >= 5
        very_dense = len(arr) >= 7
        lead_pitch = lead_pitch_by_step[step] if step < len(lead_pitch_by_step) else None

        filtered = []
        for n in arr:
            if n["dur_steps"] <= 1 and not strong and n["vel"] < 76 and n["track"] != melody_track:
                pruned += 1
                continue
            if very_dense and not eighth and n["dur_steps"] <= 1 and not n["is_top"] and n["track"] != melody_track:
                pruned += 1
                continue
            if lead_pitch is not None and n["track"] != bass_track and abs(n["pitch"] - lead_pitch) <= 1:
                pruned += 1
                continue
            if (
                lead_pitch is not None
                and n["pitch"] > lead_pitch + 5
                and not strong
                and not n["is_top"]
                and n["dur_steps"] <= 2
            ):
                pruned += 1
                continue
            filtered.append(n)
        if not filtered:
            continue

        used: Set[int] = set()
        bass_candidates = [
            i for i, n in enumerate(filtered) if n["track"] == bass_track or n["pitch"] <= LOW_ROW_MAX
        ]
        if not bass_candidates:
            bass_candidates = [0]
        keep_bass = strong or eighth or len(filtered) <= 2
        keep_bass = keep_bass or any(filtered[i]["dur_steps"] >= 5 for i in bass_candidates)
        if bass_candidates and keep_bass:
            idx = bass_candidates[0]
            bass_note = filtered[idx]
            voices["C"].append((step, bass_note["end_step"], bass_note["pitch"]))
            used.add(idx)

        remaining = [(i, n) for i, n in enumerate(filtered) if i not in used]
        if not remaining:
            continue

        if strong:
            keep = 2 if len(remaining) >= 3 and not very_dense else 1
        elif eighth and not very_dense and any(n["dur_steps"] >= 2 or n["track"] == melody_track for _, n in remaining):
            keep = 1
        elif len(remaining) == 1 and (
            remaining[0][1]["dur_steps"] >= 4 or remaining[0][1]["track"] == melody_track
        ):
            keep = 1
        else:
            keep = 0
        if keep <= 0:
            continue

        scored = []
        for idx, n in remaining:
            score = 0.0
            if n["track"] == melody_track:
                score += 1.2
            if n["is_top"]:
                score += 0.35
            score += min(0.9, 0.22 * n["dur_steps"])
            if lead_pitch is not None:
                delta = lead_pitch - n["pitch"]
                if 2 <= delta <= 12:
                    score += 1.4 - (delta / 16.0)
                elif 13 <= delta <= 18:
                    score += 0.4
                elif -2 <= delta <= 1:
                    score -= 1.0
                else:
                    score -= 0.4
            else:
                score += 0.01 * n["pitch"]
            if n["pitch"] < MID_ROW_MIN:
                score -= 0.45
            if strong and n["dur_steps"] >= 3:
                score += 0.2
            scored.append((score, idx, n))

        scored.sort(key=lambda x: (-x[0], x[2]["pitch"], x[2]["end_step"]))
        for _, idx, note in scored[:keep]:
            voices["B"].append((step, note["end_step"], note["pitch"]))

    return voices, pruned


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_analysis_sky_literal_v(\d+)\.md$",
        re.I,
    )
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_sky_literal_v{mx + 1}.md")


def key_to_midi(key: str):
    m = re.match(r"^([A-G])(\d{0,2})(#|b)?$", key)
    if not m:
        return None
    n, octv, acc = m.groups()
    o = int(octv) if octv else 5
    pc = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[n]
    if acc == "#":
        pc += 1
    elif acc == "b":
        pc -= 1
    return (o + 1) * 12 + (pc % 12)


def evaluate_txt_playability(path: str):
    text = open(path, "r", encoding="utf-8").read()
    base_pitch = 60
    for m in re.finditer(r"(?mi)\b1=([A-G]\d?\d?[#b]?)\b", text):
        maybe = key_to_midi(m.group(1))
        if maybe is not None:
            base_pitch = maybe
    total = fit = 0
    for tok in text.split():
        m = re.match(r"^(?:~)?([+\-]*)([0-7])([#b]?)([\/\-.]*)$", tok)
        if not m:
            continue
        pref, dig, semi, _ = m.groups()
        d = int(dig)
        if d == 0:
            continue
        tune = base_pitch + BASE_OFFSETS[d] + (pref.count("+") - pref.count("-")) * 12
        if semi == "#":
            tune += 1
        elif semi == "b":
            tune -= 1
        total += 1
        if tune in PLAYABLE_NOTES:
            fit += 1
    return {"notes": total, "playable": fit, "ratio": (fit / total * 100.0) if total else 0.0}


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str], extra: dict) -> None:
    lead_total = max(1, extra["lead_stats"]["lead_notes"])
    lead_track_ratio = extra["lead_stats"]["lead_from_melody_track"] / lead_total * 100.0
    lead_top_ratio = extra["lead_stats"]["lead_from_top_note"] / lead_total * 100.0
    lines = [
        f"# Analysis (Sky Literal Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Sky Literal Intent",
        "- preserve more literal rhythm/body than sky melodylock while keeping Voice A singable",
        "- force output into Sky's 15-key C4-C6 layout",
        "- keep bass and key inner motions that help recognize the original arrangement",
        "- trim same-tick middle clutter before it turns into mush on Sky input",
        f"- target layout: {SKY_LAYOUT}",
        "",
        "## Extraction Summary",
        f"- base_shift: {extra['base_shift']}",
        f"- dynamic_windows: {extra['summary']}",
        f"- lead_notes: {extra['lead_stats']['lead_notes']}",
        f"- lead_from_melody_track: {extra['lead_stats']['lead_from_melody_track']} ({lead_track_ratio:.1f}%)",
        f"- lead_from_top_note: {extra['lead_stats']['lead_from_top_note']} ({lead_top_ratio:.1f}%)",
        f"- fallback_lead_notes: {extra['lead_stats']['fallback_lead_notes']}",
        f"- lead_speed_pruned: {extra['lead_speed_pruned']}",
        f"- support_notes_pruned: {extra['support_pruned']}",
        f"- input_budget_dropped: {extra['input_budget_dropped']}",
        "",
        "## Input Stability",
        f"- clusters_per_sec_peak: {extra['stability']['clusters_per_sec_peak']}",
        f"- min_cluster_gap_ms: {extra['stability']['min_cluster_gap_ms']}",
        f"- same_key_min_gap_ms: {extra['stability']['same_key_min_gap_ms']}",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def convert_midi(input_midi: str, out_dir: str, profile_name: str) -> dict:
    p = PROFILES[profile_name]
    parsed = core.parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)

    base_shift = choose_base_shift_profile(notes, top_ids, parsed["melody_track"], tpb, p)
    shifts, win_ticks, changes = choose_dynamic_shifts_profile(
        notes, top_ids, parsed["melody_track"], tpb, base_shift, p
    )
    tick_per_step = tpb / 4.0
    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    mapped, dist = map_notes_sky(notes, shifts, win_ticks, tick_per_step)
    mapped = annotate_mapped_notes(notes, mapped, top_ids, parsed["melody_track"])

    lead_intervals, lead_ids, lead_stats = extract_melody_intervals(mapped, parsed["melody_track"])
    total_steps = max(n["end_step"] for n in mapped) + 1
    step_ms = build_step_ms(total_steps, tempo_steps)
    lead_intervals, lead_speed_pruned = prune_lead_for_input_speed(lead_intervals, step_ms)
    lead_pitch_by_step = build_active_pitch_map(lead_intervals, total_steps)

    support_voices, support_pruned = assign_support_voices(
        mapped, lead_ids, lead_pitch_by_step, parsed["melody_track"], parsed["bass_track"]
    )

    merged = {
        "A": base.merge_intervals_strict(lead_intervals),
        "B": base.merge_intervals_strict(support_voices["B"]),
        "C": base.merge_intervals_strict(support_voices["C"]),
    }
    merged, input_budget_dropped = apply_input_budget_constraints(merged, step_ms)
    stability = summarize_input_stability(merged, step_ms)

    seg_a = base.intervals_to_segments_limited(merged["A"], total_steps, 1)
    seg_b = base.intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = base.intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)

    midi_base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = base.next_script_output_path(out_dir, midi_base, "script_sky_literal")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    text = "\n".join(
        [
            f"Title: {midi_base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
            f"Source: {os.path.basename(input_midi)}",
            f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
            f"Info: profile={p.name}, {p.desc}",
            f"Info: dynamic transpose windows(4 bars): {summary}",
            f"Info: Sky 15-key layout C4-C6 -> {SKY_LAYOUT}",
            (
                "Info: speed_guard "
                f"lead_pruned={lead_speed_pruned}, support_pruned={support_pruned}, "
                f"input_budget_dropped={input_budget_dropped}, "
                f"peak_clusters/s={stability['clusters_per_sec_peak']}"
            ),
            "",
            f"bpm={tempos[0][1]}",
            "",
            "; Voice A Melody",
            *lines_a,
            "",
            "rollback=9999",
            "",
            "; Voice B Harmony",
            *lines_b,
            "",
            "rollback=9999",
            "",
            "; Voice C Bass",
            *lines_c,
            "",
        ]
    )

    issues = core.lint_domiso_text(text)
    if issues:
        raise RuntimeError(" | ".join(issues))
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    play = evaluate_txt_playability(out_path)
    return {
        "output": out_path,
        "profile": p.name,
        "notes": len(notes),
        "base_shift": base_shift,
        "changes": changes,
        "summary": summary,
        "dist": round(dist, 2),
        "play": play,
        "lead_stats": lead_stats,
        "lead_speed_pruned": lead_speed_pruned,
        "support_pruned": support_pruned,
        "input_budget_dropped": input_budget_dropped,
        "stability": stability,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Analyze + profile-select + Sky 15-key literal-balance DoMiSo conversion workflow."
    )
    sub = ap.add_subparsers(dest="cmd")

    ap_an = sub.add_parser("analyze")
    ap_an.add_argument("input_midi")
    ap_an.add_argument("--json", action="store_true")

    ap_cv = sub.add_parser("convert")
    ap_cv.add_argument("input_midi")
    ap_cv.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_cv.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))

    ap_pl = sub.add_parser("pipeline")
    ap_pl.add_argument("input_midi")
    ap_pl.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--report-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))

    ap_cp = sub.add_parser("compare")
    ap_cp.add_argument("file_a")
    ap_cp.add_argument("file_b")

    args = ap.parse_args()

    if args.cmd == "analyze":
        parsed = core.parse_midi(args.input_midi)
        metrics = analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics)
        out = {
            "input": args.input_midi,
            "recommended_profile": profile,
            "reasons": reasons,
            "metrics": metrics,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else out)
        return

    if args.cmd == "convert":
        parsed = core.parse_midi(args.input_midi)
        metrics = analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, profile)
        print(f"output={res['output']}")
        print(f"profile={res['profile']}")
        if reasons:
            print(f"profile_reasons={'; '.join(reasons)}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        metrics = analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, profile)
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(
            report,
            args.input_midi,
            metrics,
            profile,
            reasons,
            {
                "base_shift": res["base_shift"],
                "summary": res["summary"],
                "lead_stats": res["lead_stats"],
                "lead_speed_pruned": res["lead_speed_pruned"],
                "support_pruned": res["support_pruned"],
                "input_budget_dropped": res["input_budget_dropped"],
                "stability": res["stability"],
            },
        )
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={profile}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "compare":
        pa = evaluate_txt_playability(args.file_a)
        pb = evaluate_txt_playability(args.file_b)
        print(
            json.dumps(
                {
                    "A": {"path": args.file_a, "playability": pa},
                    "B": {"path": args.file_b, "playability": pb},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    legacy = argparse.ArgumentParser(description="legacy convert")
    legacy.add_argument("input_midi")
    legacy.add_argument("--out-dir", default=r"d:\domiso\txt")
    legacy.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    largs = legacy.parse_args()
    parsed = core.parse_midi(largs.input_midi)
    metrics = analyze_midi(parsed)
    profile, _ = recommend_profile(metrics) if largs.profile == "auto" else (largs.profile, [])
    res = convert_midi(largs.input_midi, largs.out_dir, profile)
    print(f"output={res['output']}")
    print(f"profile={res['profile']}")
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")


if __name__ == "__main__":
    main()
