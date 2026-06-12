#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import domiso_pipeline_literal as base
import midi_to_domiso_dense3layer as core


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
    candidate_top_n: int
    b_keep_strong: int
    b_keep_eighth: int
    b_max_poly: int
    c_max_poly: int
    offbeat_short_steps: int
    offbeat_short_vel: int
    bass_min_gap: int
    companion_min_delta: int
    companion_max_delta: int
    companion_min_dur: int
    companion_hold_steps: int
    companion_max_per_step: int
    lead_guard_semitones: int


PROFILES: Dict[str, Profile] = {
    "literal_transcription": Profile(
        "literal_transcription",
        "transcription-source literal restore: top-contour lead, anchored bass, restrained support, restored upper-mid motion",
        -10,
        10,
        0.20,
        True,
        (0, -2, -1, 1, 2),
        1,
        2,
        2,
        1,
        2,
        1,
        1,
        78,
        8,
        2,
        8,
        2,
        2,
        1,
        2,
    ),
    "literal_transcription_dense": Profile(
        "literal_transcription_dense",
        "dense transcription-source literal restore: keep more body and upper-mid flow while preventing chord-wall smear",
        -12,
        12,
        0.12,
        True,
        (0, -2, -1, 1, 2, 3),
        2,
        3,
        3,
        2,
        3,
        1,
        2,
        82,
        6,
        2,
        9,
        2,
        2,
        1,
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

    white = {0, 2, 4, 5, 7, 9, 11}
    black = sum(1 for n in notes if (n["note"] % 12) not in white)
    out_of_range = sum(1 for n in notes if n["note"] < 48 or n["note"] > 83)
    tick_per_step = tpb / 4.0
    deviations = [abs(n["start"] - round(n["start"] / tick_per_step) * tick_per_step) for n in notes]

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
        "single_note_track": len(parsed["track_medians"]) <= 1,
        "out_of_range_ratio": round(out_of_range / max(1, len(notes)), 4),
        "black_key_ratio": round(black / max(1, len(notes)), 4),
        "start_dev_median_ticks": float(statistics.median(deviations)) if deviations else 0.0,
        "start_dev_p90_ticks": float(sorted(deviations)[int(len(deviations) * 0.9)]) if deviations else 0.0,
    }


def recommend_profile(metrics: dict) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if (
        metrics["single_note_track"]
        and (
            metrics["max_poly"] >= 8
            or metrics["bar_density_p90"] >= 16
            or metrics["start_dev_p90_ticks"] >= 30
        )
    ):
        reasons.append("single-track dense piano transcription -> literal_transcription_dense")
        return "literal_transcription_dense", reasons
    reasons.append("default transcription-source literal restore profile")
    return "literal_transcription", reasons


def choose_base_shift_profile(notes: List[dict], top_ids: Set[int], tpb: int, p: Profile) -> int:
    best_shift = 0
    best_cost = float("inf")
    for shift in range(p.shift_min, p.shift_max + 1):
        total = 0.0
        for idx, n in enumerate(notes):
            _, dist = core.fold_and_snap(n["note"] + shift)
            dur = n["end"] - n["start"]
            weight = 1.0
            if idx in top_ids:
                weight += 0.9
            if dur >= tpb:
                weight += 0.3
            if dur <= max(1, tpb // 6):
                weight *= 0.75
            total += dist * weight
        total += p.shift_bias * abs(shift)
        if total < best_cost:
            best_shift = shift
            best_cost = total
    return best_shift


def choose_dynamic_shifts_profile(notes: List[dict], top_ids: Set[int], tpb: int, base_shift: int, p: Profile):
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
            for idx, n in entries:
                _, dist = core.fold_and_snap(n["note"] + shift)
                dur = n["end"] - n["start"]
                weight = 1.0 + (0.9 if idx in top_ids else 0.0) + (0.3 if dur >= tpb else 0.0)
                total += dist * weight
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
                    cost += 2.0 + 0.2 * abs(shift - prev_shift)
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


def annotate_mapped_notes(notes: List[dict], mapped_notes: List[dict], top_ids: Set[int]) -> List[dict]:
    out = []
    for idx, (src, mapped) in enumerate(zip(notes, mapped_notes)):
        row = dict(mapped)
        row["src_idx"] = idx
        row["src_note"] = src["note"]
        row["is_top"] = idx in top_ids
        out.append(row)
    return out


def collapse_same_pitch_onsets(mapped_notes: List[dict]) -> Tuple[List[dict], int]:
    grouped = defaultdict(list)
    for n in mapped_notes:
        grouped[(n["start_step"], n["pitch"])].append(n)

    collapsed = []
    reduced = 0
    for _, arr in grouped.items():
        if len(arr) == 1:
            collapsed.append(arr[0])
            continue
        reduced += len(arr) - 1
        best = max(
            arr,
            key=lambda n: (
                n["end_step"] - n["start_step"],
                n["vel"],
                n["src_note"],
                n["is_top"],
            ),
        )
        row = dict(best)
        row["end_step"] = max(n["end_step"] for n in arr)
        row["vel"] = max(n["vel"] for n in arr)
        row["is_top"] = any(n["is_top"] for n in arr)
        collapsed.append(row)
    collapsed.sort(key=lambda n: (n["start_step"], n["pitch"], n["end_step"]))
    return collapsed, reduced


def add_rank_features(mapped_notes: List[dict]) -> None:
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)
    for step, arr in by_start.items():
        ordered = sorted(arr, key=lambda n: n["pitch"], reverse=True)
        top_pitch = ordered[0]["pitch"]
        for rank, n in enumerate(ordered):
            n["rank_from_top"] = rank
            n["pitch_from_top"] = top_pitch - n["pitch"]


def score_lead_note(note: dict, prev_pitch: Optional[int], prev_end: int, step: int) -> float:
    score = 0.0
    score += max(0.0, 2.6 - 0.9 * note["rank_from_top"])
    if note["is_top"]:
        score += 0.8
    score += min(1.2, 0.22 * note["dur_steps"])
    score += min(1.0, note["vel"] / 96.0)
    if step % 4 == 0:
        score += 0.35
    elif step % 2 == 0:
        score += 0.15
    if note["pitch"] >= 60:
        score += min(1.0, (note["pitch"] - 60) * 0.05)
    else:
        score -= min(1.4, (60 - note["pitch"]) * 0.07)
    if note["dur_steps"] <= 1 and step % 2 == 1:
        score -= 0.5

    if prev_pitch is not None:
        leap = abs(note["pitch"] - prev_pitch)
        if leap <= 2:
            score += 1.0
        elif leap <= 5:
            score += 0.75
        elif leap <= 8:
            score += 0.35
        elif leap >= 17:
            score -= 1.5
        elif leap >= 12:
            score -= 0.8
        if step < prev_end and note["rank_from_top"] >= 2:
            score -= 0.9
    return score


def pick_lead_candidate(candidates: List[dict], prev_pitch: Optional[int], prev_end: int, step: int, p: Profile):
    ordered = sorted(candidates, key=lambda n: (n["pitch"], n["dur_steps"], n["vel"]), reverse=True)
    pool = ordered[: p.candidate_top_n]
    long_tail = [n for n in ordered[p.candidate_top_n :] if n["dur_steps"] >= 4 and n["pitch"] >= 60]
    pool = pool + long_tail[:2]
    scored = [(score_lead_note(n, prev_pitch, prev_end, step), n) for n in pool]
    scored.sort(key=lambda x: (x[0], x[1]["pitch"], x[1]["dur_steps"], x[1]["vel"]), reverse=True)
    return scored[0][1] if scored else None


def extract_lead_intervals(mapped_notes: List[dict], p: Profile):
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)

    lead: List[Tuple[int, int, int, int]] = []
    selected_ids: Set[int] = set()
    stats = {
        "lead_notes": 0,
        "lead_from_top_note": 0,
        "lead_from_rank1_or_2": 0,
        "fallback_lead_notes": 0,
    }
    prev_pitch: Optional[int] = None
    prev_end = -1

    for step in sorted(by_start):
        cand = pick_lead_candidate(by_start[step], prev_pitch, prev_end, step, p)
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
        if cand["rank_from_top"] == 0:
            stats["lead_from_top_note"] += 1
        elif cand["rank_from_top"] <= 2:
            stats["lead_from_rank1_or_2"] += 1
        else:
            stats["fallback_lead_notes"] += 1

        prev_pitch = cand["pitch"]
        prev_end = end

    intervals = [(s, e, pitch) for s, e, pitch, _ in lead if e > s]
    return base.merge_intervals_strict(intervals), selected_ids, stats


def build_active_pitch_map(intervals: List[Tuple[int, int, int]], total_steps: int) -> List[Optional[int]]:
    active: List[Optional[int]] = [None] * total_steps
    for start, end, pitch in intervals:
        for step in range(max(0, start), min(total_steps, end)):
            active[step] = pitch
    return active


def extract_companion_intervals(
    mapped_notes: List[dict],
    lead_ids: Set[int],
    lead_pitch_by_step: List[Optional[int]],
    p: Profile,
):
    by_start = defaultdict(list)
    for n in mapped_notes:
        if n["src_idx"] in lead_ids:
            continue
        by_start[n["start_step"]].append(n)

    intervals: List[Tuple[int, int, int]] = []
    selected_ids: Set[int] = set()
    stats = {
        "companion_notes": 0,
        "companion_on_strong": 0,
        "companion_on_offbeat": 0,
    }
    prev_pitch: Optional[int] = None
    prev_end = -1

    for step in sorted(by_start):
        lead_pitch = lead_pitch_by_step[step] if step < len(lead_pitch_by_step) else None
        if lead_pitch is None:
            continue
        lead_sustained = step + 1 < len(lead_pitch_by_step) and lead_pitch_by_step[step + 1] == lead_pitch
        strong = (step % 4) == 0
        eighth = (step % 2) == 0

        scored = []
        for n in by_start[step]:
            delta = lead_pitch - n["pitch"]
            if delta < p.companion_min_delta or delta > p.companion_max_delta:
                continue
            if n["dur_steps"] < p.companion_min_dur and not (lead_sustained or strong):
                continue
            if not (strong or eighth or lead_sustained or n["dur_steps"] >= 4):
                continue

            score = 0.0
            if 2 <= delta <= 5:
                score += 1.4
            else:
                score += 0.8
            if lead_sustained:
                score += 0.8
            if strong:
                score += 0.35
            elif eighth:
                score += 0.15
            score += min(1.0, 0.24 * n["dur_steps"])
            score += min(0.8, n["vel"] / 108.0)
            score += max(0.0, 0.4 - 0.12 * n["rank_from_top"])
            if n["pitch"] < 55:
                score -= 0.3
            if prev_pitch is not None:
                leap = abs(n["pitch"] - prev_pitch)
                if leap <= 2:
                    score += 0.55
                elif leap <= 5:
                    score += 0.35
                elif leap >= 12:
                    score -= 0.45
                if step < prev_end and leap >= 7:
                    score -= 0.35
            scored.append((score, n))

        if not scored:
            continue

        scored.sort(key=lambda x: (x[0], x[1]["pitch"], x[1]["dur_steps"], x[1]["vel"]), reverse=True)
        chosen = []
        used_pitches = set()
        for _, note in scored:
            if note["pitch"] in used_pitches:
                continue
            chosen.append(note)
            used_pitches.add(note["pitch"])
            if len(chosen) >= p.companion_max_per_step:
                break

        for note in chosen:
            c_end = max(note["end_step"], step + p.companion_hold_steps)
            intervals.append((step, c_end, note["pitch"]))
            selected_ids.add(note["src_idx"])
            stats["companion_notes"] += 1
            if strong:
                stats["companion_on_strong"] += 1
            else:
                stats["companion_on_offbeat"] += 1
            prev_pitch = note["pitch"]
            prev_end = c_end

    return base.merge_intervals_strict(intervals), selected_ids, stats


def assign_support_voices(
    mapped_notes: List[dict],
    lead_ids: Set[int],
    reserved_ids: Set[int],
    lead_pitch_by_step: List[Optional[int]],
    p: Profile,
):
    by_start = defaultdict(list)
    for n in mapped_notes:
        if n["src_idx"] in lead_ids or n["src_idx"] in reserved_ids:
            continue
        by_start[n["start_step"]].append(n)

    voices = {"B": [], "C": []}
    pruned = 0
    last_c_step = -10_000
    prev_c_pitch: Optional[int] = None

    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda n: n["pitch"])
        strong = (step % 4) == 0
        eighth = (step % 2) == 0
        dense = len(arr) >= 5
        lead_pitch = lead_pitch_by_step[step] if step < len(lead_pitch_by_step) else None

        filtered = []
        for n in arr:
            if (
                not strong
                and n["dur_steps"] <= p.offbeat_short_steps
                and n["vel"] < p.offbeat_short_vel
                and (dense or not eighth)
            ):
                pruned += 1
                continue
            if lead_pitch is not None and (lead_pitch - n["pitch"]) < p.lead_guard_semitones:
                pruned += 1
                continue
            filtered.append(n)
        if not filtered:
            continue

        bass = filtered[0]
        c_changed = prev_c_pitch is None or abs(bass["pitch"] - prev_c_pitch) >= 2
        keep_c = strong or bass["dur_steps"] >= 4 or (step - last_c_step) >= p.bass_min_gap or c_changed
        used_ids: Set[int] = set()
        if keep_c:
            c_end = max(bass["end_step"], step + (4 if strong else 2))
            voices["C"].append((step, c_end, bass["pitch"]))
            used_ids.add(bass["src_idx"])
            prev_c_pitch = bass["pitch"]
            last_c_step = step

        support = [n for n in filtered if n["src_idx"] not in used_ids]
        if not support:
            continue

        lead_sustained = step + 1 < len(lead_pitch_by_step) and lead_pitch_by_step[step + 1] == lead_pitch
        keep_b = p.b_keep_strong if strong else (p.b_keep_eighth if eighth else 0)
        if dense and not strong and keep_b > 1:
            keep_b -= 1
        if keep_b <= 0 and lead_pitch is not None and lead_sustained:
            near_lead = [
                n
                for n in support
                if p.companion_min_delta <= (lead_pitch - n["pitch"]) <= p.companion_max_delta
                and n["dur_steps"] >= p.companion_min_dur
            ]
            if near_lead:
                keep_b = 1
        if keep_b <= 0:
            continue

        scored = []
        for n in support:
            score = 0.0
            score += min(1.0, 0.20 * n["dur_steps"])
            score += min(0.8, n["vel"] / 110.0)
            if lead_pitch is not None:
                delta = lead_pitch - n["pitch"]
                if 3 <= delta <= 12:
                    score += 1.5 - delta / 16.0
                elif delta > 12:
                    score += 0.35
                else:
                    score -= 0.8
            score += max(0.0, 0.4 - 0.15 * n["rank_from_top"])
            if n["pitch"] < 52:
                score -= 0.5
            scored.append((score, n))

        scored.sort(key=lambda x: (x[0], x[1]["pitch"], x[1]["dur_steps"]), reverse=True)
        for _, note in scored[:keep_b]:
            b_end = max(note["end_step"], step + (3 if strong else 2))
            voices["B"].append((step, b_end, note["pitch"]))

    return voices, pruned


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_analysis_literal_transcription_v(\d+)\.md$",
        re.I,
    )
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_literal_transcription_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str], extra: dict) -> None:
    lead_total = max(1, extra["lead_stats"]["lead_notes"])
    top_ratio = extra["lead_stats"]["lead_from_top_note"] / lead_total * 100.0
    near_top_ratio = extra["lead_stats"]["lead_from_rank1_or_2"] / lead_total * 100.0
    lines = [
        f"# Analysis (Literal Transcription Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Transcription Intent",
        "- treat source as a single-track piano transcription rather than a clean arranged MIDI",
        "- keep a singable top contour, but preserve beat-anchored bass and harmonic body where possible",
        "- collapse same-pitch duplicates caused by transcription + playable snapping before serialization",
        "",
        "## Extraction Summary",
        f"- base_shift: {extra['base_shift']}",
        f"- dynamic_windows: {extra['summary']}",
        f"- collapsed_same_pitch_onsets: {extra['collapsed_same_pitch_onsets']}",
        f"- lead_notes: {extra['lead_stats']['lead_notes']}",
        f"- lead_from_top_note: {extra['lead_stats']['lead_from_top_note']} ({top_ratio:.1f}%)",
        f"- lead_from_rank1_or_2: {extra['lead_stats']['lead_from_rank1_or_2']} ({near_top_ratio:.1f}%)",
        f"- fallback_lead_notes: {extra['lead_stats']['fallback_lead_notes']}",
        f"- companion_notes: {extra['companion_stats']['companion_notes']}",
        f"- companion_on_strong: {extra['companion_stats']['companion_on_strong']}",
        f"- companion_on_offbeat: {extra['companion_stats']['companion_on_offbeat']}",
        f"- support_notes_pruned: {extra['support_pruned']}",
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

    base_shift = choose_base_shift_profile(notes, top_ids, tpb, p)
    shifts, win_ticks, changes = choose_dynamic_shifts_profile(notes, top_ids, tpb, base_shift, p)
    tick_per_step = tpb / 4.0
    mapped, dist = core.map_notes(notes, shifts, win_ticks, tick_per_step)
    mapped = annotate_mapped_notes(notes, mapped, top_ids)
    mapped, collapsed_same_pitch = collapse_same_pitch_onsets(mapped)
    add_rank_features(mapped)

    lead_intervals, lead_ids, lead_stats = extract_lead_intervals(mapped, p)
    total_steps = max(n["end_step"] for n in mapped) + 1
    lead_pitch_by_step = build_active_pitch_map(lead_intervals, total_steps)
    companion_intervals, companion_ids, companion_stats = extract_companion_intervals(
        mapped,
        lead_ids,
        lead_pitch_by_step,
        p,
    )
    support_voices, support_pruned = assign_support_voices(
        mapped,
        lead_ids,
        companion_ids,
        lead_pitch_by_step,
        p,
    )

    merged = {
        "A": base.merge_intervals_strict(lead_intervals),
        "B": base.merge_intervals_strict(companion_intervals + support_voices["B"]),
        "C": base.merge_intervals_strict(support_voices["C"]),
    }

    seg_a = base.intervals_to_segments_limited(merged["A"], total_steps, 1)
    seg_b = base.intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = base.intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)

    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)

    midi_base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = base.next_script_output_path(out_dir, midi_base, "script_literal_transcription")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    text = "\n".join(
        [
            f"Title: {midi_base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
            f"Source: {os.path.basename(input_midi)}",
            f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
            f"Info: profile={p.name}, {p.desc}",
            f"Info: dynamic transpose windows(4 bars): {summary}",
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

    play = base.evaluate_txt_playability(out_path)
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
        "companion_stats": companion_stats,
        "support_pruned": support_pruned,
        "collapsed_same_pitch_onsets": collapsed_same_pitch,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Analyze + profile-select + transcription-source literal DoMiSo conversion workflow."
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
                "companion_stats": res["companion_stats"],
                "support_pruned": res["support_pruned"],
                "collapsed_same_pitch_onsets": res["collapsed_same_pitch_onsets"],
            },
        )
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={profile}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "compare":
        pa = base.evaluate_txt_playability(args.file_a)
        pb = base.evaluate_txt_playability(args.file_b)
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
