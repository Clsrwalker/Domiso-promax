#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import midi_to_domiso_dense3layer as core


PLAYABLE_NOTES = {
    48, 50, 52, 53, 55, 57, 59,
    60, 62, 64, 65, 67, 69, 71,
    72, 74, 76, 77, 79, 81, 83,
}
BASE_OFFSETS = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}


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
    melody_mode: str  # "contour" or "top"
    a_harmony: bool
    b_keep_strong: int
    b_keep_normal: int
    c_dense_offbeat: bool
    short_nonmel_steps: int
    short_nonmel_vel: int
    a_max_poly: int
    b_max_poly: int
    c_max_poly: int
    human_delay_steps: int
    human_lag_ratio: float
    human_release_ratio: float
    human_pickup_ratio: float
    melody_breath_every: int
    melody_breath_gap: int


PROFILES: Dict[str, Profile] = {
    "longnote_solo": Profile(
        "longnote_solo", "long-note melody first, very sparse accompaniment",
        -4, 4, 2.4, False, (0,), 0, "contour", False, 1, 0, False, 2, 86, 1, 1, 1,
        1, 0.34, 0.24, 0.16, 24, 1
    ),
    "longnote_balanced": Profile(
        "longnote_balanced", "long-note priority with richer but controlled 3-layer support",
        -6, 6, 1.8, True, (0, -2, -1, 1, 2), 2, "contour", False, 2, 1, False, 1, 76, 1, 1, 1,
        1, 0.28, 0.20, 0.14, 20, 1
    ),
    "longnote_dense": Profile(
        "longnote_dense", "dense source with sustained contour and fuller harmony bed",
        -8, 8, 1.2, True, (0, -2, -1, 1, 2, 3), 3, "contour", False, 2, 1, False, 1, 74, 1, 1, 1,
        1, 0.22, 0.16, 0.10, 18, 1
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
    reasons = []
    if metrics["note_count"] > 1400 or metrics["max_poly"] >= 6 or metrics["bar_density_p90"] >= 14:
        reasons.append("high density/polyphony -> keep long-note contour while filtering ornaments")
        return "longnote_dense", reasons
    if metrics["tempo0"] >= 145 and metrics["note_count"] >= 650:
        reasons.append("fast and note-rich -> balanced long-note profile")
        return "longnote_balanced", reasons
    if metrics["time_sig"] == "3/4" and metrics["tracks"] <= 2:
        reasons.append("3/4 + few tracks -> longnote_solo keeps waltz lines clean")
        return "longnote_solo", reasons
    reasons.append("default longnote-balanced profile")
    return "longnote_balanced", reasons


def choose_base_shift_profile(notes: List[dict], top_ids: set, melody_track: int, tpb: int, p: Profile) -> int:
    best_s, best_c = 0, float("inf")
    for s in range(p.shift_min, p.shift_max + 1):
        c = core.evaluate_shift_cost(notes, s, top_ids, melody_track, tpb) + p.shift_bias * abs(s)
        if c < best_c:
            best_s, best_c = s, c
    return best_s


def choose_dynamic_shifts_profile(notes: List[dict], top_ids: set, melody_track: int, tpb: int, base: int, p: Profile):
    win_ticks = max(1, tpb * 16)
    max_win = max(n["start"] // win_ticks for n in notes)
    cnt = max_win + 1
    if not p.dynamic:
        return [base] * cnt, win_ticks, 0
    cands = sorted({base + d for d in p.dynamic_offsets if p.shift_min <= base + d <= p.shift_max} | {base})
    by_w = defaultdict(list)
    for i, n in enumerate(notes):
        by_w[n["start"] // win_ticks].append((i, n))
    local = []
    for w in range(cnt):
        entries = by_w.get(w, [])
        vals = {}
        for s in cands:
            total = 0.0
            for gi, n in entries:
                _, dist = core.fold_and_snap(n["note"] + s)
                wt = 1.0 + (0.8 if gi in top_ids else 0.0) + (0.25 if n["track"] == melody_track else 0.0)
                total += dist * wt
            vals[s] = total
        local.append(vals)
    dp = {(s, 0): local[0][s] for s in cands}
    back = [{(s, 0): None for s in cands}]
    for w in range(1, cnt):
        ndp, nb = {}, {}
        for s in cands:
            for (ps, ch), pc in dp.items():
                nch = ch + (1 if s != ps else 0)
                if nch > p.max_changes:
                    continue
                cost = pc + local[w][s] + (2.5 if s != ps else 0.0) + 0.3 * abs(s - ps)
                key = (s, nch)
                if key not in ndp or cost < ndp[key]:
                    ndp[key] = cost
                    nb[key] = (ps, ch)
        if not ndp:
            ndp = {(base, 0): min(dp.values())}
            nb = {(base, 0): min(dp, key=lambda k: dp[k])}
        dp = ndp
        back.append(nb)
    state = min(dp, key=lambda k: dp[k])
    shifts = [base] * cnt
    for w in range(cnt - 1, -1, -1):
        shifts[w] = state[0]
        prev = back[w].get(state)
        if prev is None:
            break
        state = prev
    changes = sum(1 for i in range(1, len(shifts)) if shifts[i] != shifts[i - 1])
    return shifts, win_ticks, changes


def intervals_to_segments_limited(intervals: List[Tuple[int, int, int]], total_steps: int, max_poly: int):
    starts = defaultdict(list)
    ends = defaultdict(list)
    for s, e, pitch in intervals:
        s = max(0, s)
        e = min(total_steps, e)
        if e <= s:
            continue
        starts[s].append(pitch)
        ends[e].append(pitch)

    active = Counter()
    segments = []
    prev_key = None
    seg_start = 0

    for step in range(total_steps):
        for p in ends.get(step, []):
            active[p] -= 1
            if active[p] <= 0:
                del active[p]
        for p in starts.get(step, []):
            active[p] += 1

        pitches = sorted(active.keys())
        if max_poly <= 0:
            pitches = []
        elif len(pitches) > max_poly:
            pitches = pitches[-max_poly:]

        key = tuple(pitches)
        if prev_key is None:
            prev_key = key
            seg_start = step
        elif key != prev_key:
            segments.append((seg_start, step, prev_key))
            seg_start = step
            prev_key = key

    if prev_key is None:
        return [(0, total_steps, tuple())]
    segments.append((seg_start, total_steps, prev_key))
    return segments


def assign_voices_profile(mapped_notes: List[dict], melody_track: int, bass_track: int, p: Profile):
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)
    voices = {"A": [], "B": [], "C": []}
    prev_a = None
    removed = 0
    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda x: (x["pitch"], x["track"]))
        filt = []
        for n in arr:
            if (
                n["track"] != melody_track
                and n["dur_steps"] <= p.short_nonmel_steps
                and ((step % 2 == 1) or (n["vel"] < p.short_nonmel_vel))
            ):
                removed += 1
                continue
            filt.append(n)
        if not filt:
            continue
        used = set()
        strong = (step % 4) == 0
        eighth = (step % 2) == 0
        dense = len(filt) >= 5
        a_idx = None
        if p.melody_mode == "contour":
            mel = [i for i, n in enumerate(filt) if n["track"] == melody_track]
            if mel:
                if prev_a is None:
                    a_idx = max(mel, key=lambda i: filt[i]["pitch"])
                else:
                    a_idx = min(
                        mel,
                        key=lambda i: (abs(filt[i]["pitch"] - prev_a), -filt[i]["pitch"]),
                    )
        else:
            a_idx = len(filt) - 1
        if a_idx is not None:
            a = filt[a_idx]
            # Keep melody notes sustained (minimum 1/8 beat) to avoid ornament-like chopping.
            a_end = max(a["end_step"], step + 2)
            voices["A"].append((step, a_end, a["pitch"]))
            used.add(a_idx)
            prev_a = a["pitch"]
        if a_idx is not None and p.a_harmony and strong and len(filt) >= 4:
            for i in range(len(filt) - 2, -1, -1):
                if i in used:
                    continue
                iv = filt[a_idx]["pitch"] - filt[i]["pitch"]
                if 3 <= iv <= 8:
                    n = filt[i]
                    voices["A"].append((step, n["end_step"], n["pitch"]))
                    used.add(i)
                    break
        cands = [i for i, n in enumerate(filt) if i not in used and (n["track"] == bass_track or n["pitch"] <= 60)]
        if not cands:
            cands = [i for i in range(len(filt)) if i not in used]
        if cands and (p.c_dense_offbeat or not dense or strong or eighth):
            i = cands[0]
            n = filt[i]
            c_end = max(n["end_step"], step + (3 if strong else 2))
            voices["C"].append((step, c_end, n["pitch"]))
            used.add(i)
        rem = [(i, n) for i, n in enumerate(filt) if i not in used]
        if rem:
            if dense and not p.c_dense_offbeat and not (strong or eighth):
                rem = []
            keep = p.b_keep_strong if strong else p.b_keep_normal
            if not eighth and not strong:
                keep = 0
            keep = max(0, min(keep, len(rem)))
            if keep > 0:
                # Prefer longer notes in B to avoid turning sustained harmony into ornaments.
                rem_sorted = sorted(
                    rem,
                    key=lambda pair: (pair[1]["dur_steps"], pair[1]["pitch"]),
                    reverse=True,
                )
                for i in range(keep):
                    _, n = rem_sorted[i]
                    b_end = max(n["end_step"], step + (3 if strong else (2 if eighth else 1)))
                    voices["B"].append((step, b_end, n["pitch"]))
    return voices, removed


def build_window_steps() -> int:
    # 4 bars * 4 beats * 4 steps/beat
    return 64


def classify_density_windows(mapped_notes: List[dict], win_steps: int) -> Dict[int, str]:
    cnt = Counter(n["start_step"] // win_steps for n in mapped_notes)
    if not cnt:
        return {}
    vals = sorted(cnt.values())
    p30 = vals[max(0, int(len(vals) * 0.30) - 1)]
    p75 = vals[max(0, int(len(vals) * 0.75) - 1)]
    out: Dict[int, str] = {}
    for w, c in cnt.items():
        if c <= p30:
            out[w] = "thin"
        elif c >= p75:
            out[w] = "full"
        else:
            out[w] = "mid"
    return out


def build_style_windows(density: Dict[int, str], tempo0: int) -> Dict[int, str]:
    styles: Dict[int, str] = {}
    for w, d in density.items():
        if d == "thin":
            styles[w] = "bass_chord"
        elif d == "full":
            styles[w] = "arp16" if tempo0 < 150 else "arp8"
        else:
            styles[w] = "arp8" if tempo0 < 138 else "block"
    return styles


def build_pocket_windows(density: Dict[int, str], tempo0: int) -> Dict[int, str]:
    pocket: Dict[int, str] = {}
    for w, d in density.items():
        if tempo0 <= 108 or d == "thin":
            pocket[w] = "back"
        elif tempo0 >= 152:
            pocket[w] = "front"
        else:
            pocket[w] = "straight"
    return pocket


def choose_melody_note(arr: List[dict], prev_a: int | None, melody_track: int) -> dict:
    top = arr[max(0, len(arr) - 4):]
    if not top:
        return arr[-1]

    def score(n: dict) -> float:
        s = 0.0
        s += 2.0 if n["track"] == melody_track else 0.0
        s += 0.25 * min(8, n["dur_steps"])
        s += 0.015 * n["vel"]
        s += 0.04 * n["pitch"]
        if prev_a is not None:
            jump = abs(n["pitch"] - prev_a)
            s -= 0.20 * jump
            if jump > 10:
                s -= 1.2
        return s

    return max(top, key=score)


def assign_voices_literal_human(
    mapped_notes: List[dict],
    melody_track: int,
    bass_track: int,
    p: Profile,
    win_steps: int,
    density_map: Dict[int, str],
):
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)

    voices = {"A": [], "B": [], "C": []}
    prev_a = None
    removed = 0
    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda x: (x["pitch"], x["track"]))
        if not arr:
            continue
        win = step // win_steps
        band = density_map.get(win, "mid")
        strong = (step % 4) == 0
        weak = (step % 2) == 0 and not strong

        # Keep longnote behavior: strip short non-mel weak noise first.
        filt = []
        for n in arr:
            if (
                n["track"] != melody_track
                and n["dur_steps"] <= p.short_nonmel_steps
                and ((step % 2 == 1) or (n["vel"] < p.short_nonmel_vel))
            ):
                removed += 1
                continue
            filt.append(n)
        if not filt:
            continue

        mel = choose_melody_note(filt, prev_a, melody_track)
        a_end = max(mel["end_step"], step + (3 if strong else 2))
        voices["A"].append((step, a_end, mel["pitch"]))
        prev_a = mel["pitch"]

        lows = [n for n in filt if (n["track"] == bass_track or n["pitch"] <= 60)]
        lo = lows[0] if lows else min(filt, key=lambda n: n["pitch"])
        c_end = max(lo["end_step"], step + (3 if strong else 2))
        voices["C"].append((step, c_end, lo["pitch"]))

        mids = [n for n in filt if n is not mel and n is not lo]
        if not mids:
            continue
        if band == "thin":
            keep = 1 if strong else 0
        elif band == "full":
            keep = 3 if strong else (1 if weak else 0)
        else:
            keep = 2 if strong else (1 if weak else 0)
        mids_sorted = sorted(mids, key=lambda n: (n["dur_steps"], n["vel"], n["pitch"]), reverse=True)
        for n in mids_sorted[:keep]:
            b_end = max(n["end_step"], step + (2 if weak else 1))
            voices["B"].append((step, b_end, n["pitch"]))
        removed += max(0, len(mids_sorted) - keep)

    return voices, removed


def normalize_ratio(v: float) -> float:
    return max(0.0, min(1.0, float(v)))


def hash_gate(step: int, pitch: int, ratio: float, salt: int = 0) -> bool:
    if ratio <= 0.0:
        return False
    h = ((step * 1315423911) ^ (pitch * 2654435761) ^ salt) & 0xFFFFFFFF
    return (h % 1000) < int(ratio * 1000.0)


def apply_melody_breath(
    intervals: List[Tuple[int, int, int]],
    every_steps: int,
    gap_steps: int,
    jump_trigger: int = 8,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    every_steps = max(1, int(every_steps))
    gap_steps = max(0, int(gap_steps))
    if gap_steps <= 0:
        return intervals, 0

    arr = sorted(intervals, key=lambda x: (x[0], x[1], x[2]))
    out: List[Tuple[int, int, int]] = []
    phrase_steps = 0
    cuts = 0
    for i, (s, e, pitch) in enumerate(arr):
        if e <= s:
            continue
        if out and s < out[-1][1]:
            s = out[-1][1]
            if e <= s:
                continue

        dur = e - s
        phrase_steps += dur
        cut = 0
        if i + 1 < len(arr):
            ns, _, np = arr[i + 1]
            jump = abs(np - pitch)
            if jump >= jump_trigger and ns <= e:
                cut = max(cut, gap_steps)
            if phrase_steps >= every_steps and ns <= e:
                cut = max(cut, gap_steps)
        if cut > 0:
            ne = max(s + 1, e - cut)
            if ne < e:
                e = ne
                phrase_steps = 0
                cuts += 1
        out.append((s, e, pitch))
    return core.merge_intervals(out), cuts


def apply_support_lag(
    intervals: List[Tuple[int, int, int]],
    melody_starts: set,
    delay_steps: int,
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    delay_steps = max(0, int(delay_steps))
    ratio = normalize_ratio(ratio)
    if delay_steps <= 0 or ratio <= 0.0:
        return intervals, 0

    out: List[Tuple[int, int, int]] = []
    hits = 0
    for s, e, pitch in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        dur = e - s
        if s not in melody_starts or dur < 3:
            out.append((s, e, pitch))
            continue
        local_ratio = ratio * (0.65 if (s % 4) == 0 else 1.0)
        if not hash_gate(s, pitch, local_ratio, salt=0x51ED270B):
            out.append((s, e, pitch))
            continue
        ns = s + delay_steps
        ne = max(ns + 1, e)
        out.append((ns, ne, pitch))
        hits += 1
    return core.merge_intervals(out), hits


def apply_pickup_push(
    intervals: List[Tuple[int, int, int]],
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    ratio = normalize_ratio(ratio)
    if ratio <= 0.0:
        return intervals, 0

    arr = sorted(intervals, key=lambda x: (x[0], x[2], x[1]))
    out: List[Tuple[int, int, int]] = []
    moves = 0
    prev_end = 0
    for s, e, pitch in arr:
        if e <= s:
            continue
        dur = e - s
        weak_pickup = (s % 4) in (1, 3)
        local_ratio = ratio * (1.0 if (s % 4) == 3 else 0.55)
        can_push = weak_pickup and dur >= 2 and s > 0
        if can_push and hash_gate(s, pitch, local_ratio, salt=0x85EBCA77):
            ns = max(prev_end, s - 1)
            if ns >= s:
                out.append((s, e, pitch))
                prev_end = max(prev_end, e)
                continue
            ne = max(ns + 1, e - 1)
            if ns < s:
                s, e = ns, ne
                moves += 1
        out.append((s, e, pitch))
        prev_end = max(prev_end, e)
    return core.merge_intervals(out), moves


def apply_human_release(
    intervals: List[Tuple[int, int, int]],
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    ratio = normalize_ratio(ratio)
    if ratio <= 0.0:
        return intervals, 0

    out: List[Tuple[int, int, int]] = []
    hits = 0
    for s, e, pitch in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        dur = e - s
        weak = (s % 4) != 0
        if weak and dur >= 4 and hash_gate(s, pitch, ratio, salt=0xC2B2AE35):
            ne = max(s + 1, e - 1)
            if ne < e:
                e = ne
                hits += 1
        out.append((s, e, pitch))
    return core.merge_intervals(out), hits


def enforce_legato_floor(
    intervals: List[Tuple[int, int, int]],
    min_steps: int,
    weak_extra: int = 0,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    min_steps = max(1, int(min_steps))
    weak_extra = max(0, int(weak_extra))
    out: List[Tuple[int, int, int]] = []
    changed = 0
    for s, e, p in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        ne = e
        if ne - s < min_steps:
            ne = s + min_steps
        if weak_extra > 0 and (s % 4) != 0:
            ne += weak_extra
        if ne != e:
            changed += 1
        out.append((s, ne, p))
    return core.merge_intervals(out), changed


def apply_style_library(
    b_intervals: List[Tuple[int, int, int]],
    style_windows: Dict[int, str],
    win_steps: int,
) -> Tuple[List[Tuple[int, int, int]], Dict[str, int]]:
    if not b_intervals:
        return b_intervals, {"block": 0, "bass_chord": 0, "arp8": 0, "arp16": 0}
    by_start = defaultdict(list)
    for s, e, p in b_intervals:
        if e > s:
            by_start[s].append((s, e, p))
    out: List[Tuple[int, int, int]] = []
    stats = {"block": 0, "bass_chord": 0, "arp8": 0, "arp16": 0}
    for step in sorted(by_start):
        group = sorted(by_start[step], key=lambda x: x[2])
        style = style_windows.get(step // win_steps, "block")
        stats[style] = stats.get(style, 0) + 1
        if len(group) <= 1 or style == "block":
            out.extend(group)
            continue
        if style == "bass_chord":
            out.append(group[0])
            for s, e, p in group[1:]:
                ns = s + 1
                out.append((ns, max(ns + 1, e), p))
            continue
        spacing = 2 if style == "arp8" else 1
        for idx, (s, e, p) in enumerate(group):
            ns = s + idx * spacing
            ne = max(ns + 1, e)
            out.append((ns, ne, p))
    return core.merge_intervals(out), stats


def apply_pocket(
    intervals: List[Tuple[int, int, int]],
    pocket_windows: Dict[int, str],
    win_steps: int,
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    ratio = normalize_ratio(ratio)
    out: List[Tuple[int, int, int]] = []
    hits = 0
    for s, e, p in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        pocket = pocket_windows.get(s // win_steps, "straight")
        ns, ne = s, e
        if pocket == "back" and (s % 4) in (1, 2, 3) and hash_gate(s, p, ratio, salt=0x7F4A7C15):
            ns = s + 1
            ne = max(ns + 1, e)
            hits += 1
        elif pocket == "front" and (s % 4) == 3 and s > 0 and hash_gate(s, p, ratio * 0.8, salt=0x165667B1):
            ns = s - 1
            ne = max(ns + 1, e - 1)
            hits += 1
        out.append((ns, ne, p))
    return core.merge_intervals(out), hits


def detect_repeat_windows(a_intervals: List[Tuple[int, int, int]], win_steps: int) -> Set[int]:
    by_w = defaultdict(list)
    for s, _, p in sorted(a_intervals, key=lambda x: (x[0], x[2], x[1])):
        by_w[s // win_steps].append((s, p))
    sig_map: Dict[Tuple[int, ...], List[int]] = defaultdict(list)
    for w in sorted(by_w):
        arr = by_w[w][:10]
        if len(arr) < 4:
            continue
        pitches = [p for _, p in arr]
        diffs = [max(-7, min(7, pitches[i] - pitches[i - 1])) for i in range(1, len(pitches))]
        sig = tuple(diffs[:8])
        sig_map[sig].append(w)
    repeated: Set[int] = set()
    for ws in sig_map.values():
        if len(ws) > 1:
            repeated.update(ws[1:])
    return repeated


def apply_repeat_variation(
    a_intervals: List[Tuple[int, int, int]],
    b_intervals: List[Tuple[int, int, int]],
    c_intervals: List[Tuple[int, int, int]],
    repeated_windows: Set[int],
    win_steps: int,
) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]], List[Tuple[int, int, int]], int]:
    if not repeated_windows:
        return a_intervals, b_intervals, c_intervals, 0
    changed = 0
    a2: List[Tuple[int, int, int]] = []
    for s, e, p in a_intervals:
        w = s // win_steps
        if w in repeated_windows and (s % 4) in (2, 3) and e - s >= 3 and hash_gate(s, p, 0.35, salt=0x27D4EB2F):
            ne = max(s + 1, e - 1)
            if ne < e:
                e = ne
                changed += 1
        a2.append((s, e, p))

    def vary_mid(intervals: List[Tuple[int, int, int]], ratio: float, salt: int):
        nonlocal changed
        out = []
        for s, e, p in intervals:
            w = s // win_steps
            if w in repeated_windows and (s % 4) != 0 and hash_gate(s, p, ratio, salt=salt):
                if (e - s) <= 2:
                    changed += 1
                    continue
                ns = s + 1
                out.append((ns, max(ns + 1, e), p))
                changed += 1
            else:
                out.append((s, e, p))
        return out

    b2 = vary_mid(b_intervals, 0.28, 0x9E3779B9)
    c2 = vary_mid(c_intervals, 0.15, 0x85EBCA77)
    return core.merge_intervals(a2), core.merge_intervals(b2), core.merge_intervals(c2), changed


def apply_hand_constraints(
    voices: Dict[str, List[Tuple[int, int, int]]],
    left_hand_max: int = 3,
    right_hand_max: int = 3,
    hand_max_jump: int = 10,
    hand_min_react_steps: int = 2,
) -> Tuple[Dict[str, List[Tuple[int, int, int]]], int]:
    events = []
    for v in ("A", "B", "C"):
        for idx, (s, e, pitch) in enumerate(voices[v]):
            if e > s:
                events.append({"voice": v, "idx": idx, "s": s, "e": e, "pitch": pitch})
    by_step = defaultdict(list)
    for ev in events:
        by_step[ev["s"]].append(ev)

    drop = set()
    for step in sorted(by_step):
        arr = [ev for ev in by_step[step] if (ev["voice"], ev["idx"]) not in drop]
        right = [ev for ev in arr if ev["voice"] == "A" or (ev["voice"] == "B" and ev["pitch"] >= 64)]
        left = [ev for ev in arr if ev["voice"] == "C" or (ev["voice"] == "B" and ev["pitch"] < 64)]
        for hand_arr, max_n, center in ((right, right_hand_max, 72), (left, left_hand_max, 55)):
            if len(hand_arr) <= max_n:
                continue
            extras = len(hand_arr) - max_n
            hand_arr.sort(key=lambda ev: (0 if ev["voice"] == "B" else 1, -abs(ev["pitch"] - center)))
            for ev in hand_arr[:extras]:
                drop.add((ev["voice"], ev["idx"]))

    prev = {"left": None, "right": None}
    for step in sorted(by_step):
        arr = [ev for ev in by_step[step] if (ev["voice"], ev["idx"]) not in drop]
        hand_map = {
            "left": [ev for ev in arr if ev["voice"] == "C" or (ev["voice"] == "B" and ev["pitch"] < 64)],
            "right": [ev for ev in arr if ev["voice"] == "A" or (ev["voice"] == "B" and ev["pitch"] >= 64)],
        }
        for hand in ("left", "right"):
            cand = hand_map[hand]
            if not cand:
                continue
            if prev[hand] is None:
                pick = min(cand, key=lambda ev: ev["pitch"]) if hand == "left" else max(cand, key=lambda ev: ev["pitch"])
                prev[hand] = (step, pick["pitch"])
                continue
            ps, pp = prev[hand]
            if step - ps > hand_min_react_steps:
                pick = min(cand, key=lambda ev: abs(ev["pitch"] - pp))
                prev[hand] = (step, pick["pitch"])
                continue
            feasible = [ev for ev in cand if abs(ev["pitch"] - pp) <= hand_max_jump]
            if feasible:
                pick = min(feasible, key=lambda ev: abs(ev["pitch"] - pp))
                prev[hand] = (step, pick["pitch"])
                for ev in cand:
                    if ev is pick:
                        continue
                    if ev["voice"] == "B" and abs(ev["pitch"] - pp) > hand_max_jump:
                        drop.add((ev["voice"], ev["idx"]))
                continue
            for ev in cand:
                if ev["voice"] == "B":
                    drop.add((ev["voice"], ev["idx"]))

    out = {"A": [], "B": [], "C": []}
    for ev in events:
        if (ev["voice"], ev["idx"]) in drop:
            continue
        out[ev["voice"]].append((ev["s"], ev["e"], ev["pitch"]))
    return {k: core.merge_intervals(v) for k, v in out.items()}, len(drop)


def build_phrase_ranges(a_intervals: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    arr = sorted(a_intervals, key=lambda x: (x[0], x[1], x[2]))
    if not arr:
        return []
    ranges: List[Tuple[int, int]] = []
    cur_s = arr[0][0]
    cur_e = arr[0][1]
    prev_pitch = arr[0][2]
    for s, e, pitch in arr[1:]:
        gap = s - cur_e
        jump = abs(pitch - prev_pitch)
        if gap >= 4 or jump >= 8:
            ranges.append((cur_s, cur_e))
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
        prev_pitch = pitch
    ranges.append((cur_s, cur_e))
    return ranges


def build_rubato_tempo_steps(
    tempo_steps: List[Tuple[int, int]],
    phrase_ranges: List[Tuple[int, int]],
    depth_bpm: int,
) -> List[Tuple[int, int]]:
    if not tempo_steps or not phrase_ranges or depth_bpm <= 0:
        return tempo_steps
    base_map = sorted(tempo_steps)
    # If the source itself has many tempo nodes, avoid adding rubato jitter.
    if len(base_map) >= 5:
        return tempo_steps

    def bpm_at(step: int) -> int:
        bpm = base_map[0][1]
        for s, b in base_map:
            if s > step:
                break
            bpm = b
        return bpm

    base_change_steps = {s for s, _ in base_map}

    def near_base_change(step: int, margin: int = 6) -> bool:
        for bs in base_change_steps:
            if bs == 0:
                continue
            if abs(step - bs) <= margin:
                return True
        return False

    extra: List[Tuple[int, int]] = []
    d = max(1, min(5, int(depth_bpm)))
    for s, e in phrase_ranges:
        ln = e - s
        # Keep source tempo boundaries and short phrases stable.
        if ln < 12 or near_base_change(s) or near_base_change(e):
            continue
        base = bpm_at(s)
        head = max(20, base - d)
        tail = max(20, base - max(1, d - 1))
        mid = s + max(2, ln // 3)
        pre_end = max(s + 2, e - max(2, ln // 6))
        extra.extend([(s, head), (mid, base), (pre_end, tail), (e, base)])

    merged = list(base_map) + extra
    merged.sort(key=lambda x: (x[0], x[1]))

    out: List[Tuple[int, int]] = []
    for step, bpm in merged:
        bpm = max(20, min(480, int(bpm)))
        if out and out[-1][0] == step:
            out[-1] = (step, bpm)
        elif not out or out[-1][1] != bpm:
            out.append((step, bpm))
    if not out:
        return tempo_steps

    # Smooth only mild jumps; avoid over-shaping major structural tempo boundaries.
    smooth: List[Tuple[int, int]] = [out[0]]
    max_delta_per_node = 2
    for step, bpm in out[1:]:
        prev_step, prev_bpm = smooth[-1]
        if step <= prev_step:
            if step == prev_step:
                smooth[-1] = (step, bpm)
            continue

        delta = bpm - prev_bpm
        span = step - prev_step
        if abs(delta) > 6 or prev_step in base_change_steps or step in base_change_steps:
            seg = 1
        else:
            seg_need = max(1, (abs(delta) + max_delta_per_node - 1) // max_delta_per_node)
            seg = min(seg_need, max(1, span), 3)
        if seg > 1:
            for i in range(1, seg):
                ns = prev_step + round(span * i / seg)
                nb = prev_bpm + round(delta * i / seg)
                nb = max(20, min(480, int(nb)))
                if ns <= smooth[-1][0]:
                    continue
                if smooth[-1][1] == nb:
                    continue
                smooth.append((ns, nb))

        bpm = max(20, min(480, int(bpm)))
        if smooth and smooth[-1][0] == step:
            smooth[-1] = (step, bpm)
        elif not smooth or smooth[-1][1] != bpm:
            smooth.append((step, bpm))
    return smooth


def coarsen_tempo_steps(
    tempo_steps: List[Tuple[int, int]],
    min_gap_steps: int,
    min_bpm_delta: int,
) -> List[Tuple[int, int]]:
    if not tempo_steps:
        return tempo_steps
    out = [tempo_steps[0]]
    for step, bpm in tempo_steps[1:]:
        ps, pb = out[-1]
        if (step - ps) < min_gap_steps and abs(bpm - pb) < min_bpm_delta:
            continue
        if out and out[-1][1] == bpm:
            continue
        out.append((step, bpm))
    return out


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
    base = 60
    for m in re.finditer(r"(?mi)\b1=([A-G]\d?\d?[#b]?)\b", text):
        maybe = key_to_midi(m.group(1))
        if maybe is not None:
            base = maybe
    total = fit = 0
    for tok in text.split():
        m = re.match(r"^(?:~)?([+\-]*)([0-7])([#b]?)([\/\-.]*)$", tok)
        if not m:
            continue
        pref, dig, semi, _ = m.groups()
        d = int(dig)
        if d == 0:
            continue
        tune = base + BASE_OFFSETS[d] + (pref.count("+") - pref.count("-")) * 12
        if semi == "#":
            tune += 1
        elif semi == "b":
            tune -= 1
        total += 1
        if tune in PLAYABLE_NOTES:
            fit += 1
    return {"notes": total, "playable": fit, "ratio": (fit / total * 100.0) if total else 0.0}


def next_script_output_path(out_dir: str, midi_base: str, script_name: str):
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(out_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_domiso_" + re.escape(script_name) + r"_v(\d+)\.txt$",
        re.I,
    )
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_domiso_{script_name}_v{mx + 1}.txt")


def convert_midi(
    input_midi: str,
    out_dir: str,
    profile_name: str,
    humanize: bool = True,
    human_mode: str = "sad",
    human_delay_steps: int | None = None,
    human_lag_ratio: float | None = None,
    human_release_ratio: float | None = None,
    human_pickup_ratio: float | None = None,
    melody_breath_every: int | None = None,
    melody_breath_gap: int | None = None,
):
    p = PROFILES[profile_name]
    mode = (human_mode or "sad").lower()
    if mode not in {"sad", "lite", "full"}:
        mode = "sad"

    if mode == "sad":
        rubato_depth = 1
        lag_scale = 0.12
        rel_scale = 0.0
        pickup_scale = 0.0
    elif mode == "lite":
        rubato_depth = 0
        lag_scale = 0.32
        rel_scale = 0.28
        pickup_scale = 0.18
    else:
        rubato_depth = 2
        lag_scale = 1.00
        rel_scale = 1.00
        pickup_scale = 1.00

    human_delay_steps = (0 if mode == "sad" else p.human_delay_steps) if human_delay_steps is None else max(0, int(human_delay_steps))
    human_lag_ratio = normalize_ratio((p.human_lag_ratio * lag_scale) if human_lag_ratio is None else human_lag_ratio)
    human_release_ratio = normalize_ratio((p.human_release_ratio * rel_scale) if human_release_ratio is None else human_release_ratio)
    human_pickup_ratio = normalize_ratio((p.human_pickup_ratio * pickup_scale) if human_pickup_ratio is None else human_pickup_ratio)
    if melody_breath_every is None:
        melody_breath_every = p.melody_breath_every + 10 if mode == "sad" else (p.melody_breath_every + 6 if mode == "lite" else p.melody_breath_every)
    else:
        melody_breath_every = max(1, int(melody_breath_every))
    if melody_breath_gap is None:
        melody_breath_gap = 0 if mode == "sad" else p.melody_breath_gap
    else:
        melody_breath_gap = max(0, int(melody_breath_gap))

    parsed = core.parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)
    base_shift = choose_base_shift_profile(notes, top_ids, parsed["melody_track"], tpb, p)
    shifts, win_ticks, changes = choose_dynamic_shifts_profile(notes, top_ids, parsed["melody_track"], tpb, base_shift, p)
    tick_per_step = tpb / 4.0
    mapped, dist = core.map_notes(notes, shifts, win_ticks, tick_per_step)
    win_steps = build_window_steps()
    density = classify_density_windows(mapped, win_steps)
    style_windows = build_style_windows(density, tempos[0][1])
    pocket_windows = build_pocket_windows(density, tempos[0][1])

    if mode == "lite":
        voices, removed = assign_voices_profile(mapped, parsed["melody_track"], parsed["bass_track"], p)
    else:
        voices, removed = assign_voices_literal_human(
            mapped, parsed["melody_track"], parsed["bass_track"], p, win_steps, density
        )
    merged = {k: core.merge_intervals(v) for k, v in voices.items()}

    style_stats = {"block": 0, "bass_chord": 0, "arp8": 0, "arp16": 0}
    pocket_hits = 0
    repeat_hits = 0
    hand_drop = 0
    lag_hits = 0
    pickup_hits = 0
    release_hits = 0
    legato_hits = 0

    if humanize:
        merged["A"], breath_hits = apply_melody_breath(merged["A"], melody_breath_every, melody_breath_gap)

        use_style = mode == "full"
        use_repeat = mode == "full"
        use_hand = mode == "full"
        use_pocket = mode == "full"
        use_pickup_push = mode == "full"

        if use_style:
            merged["B"], style_stats = apply_style_library(merged["B"], style_windows, win_steps)

        if use_pocket:
            merged["B"], p_b = apply_pocket(merged["B"], pocket_windows, win_steps, human_pickup_ratio)
            pocket_hits += p_b
            bass_pocket_ratio = human_pickup_ratio * 0.60
            merged["C"], p_c = apply_pocket(merged["C"], pocket_windows, win_steps, bass_pocket_ratio)
            pocket_hits += p_c

        if use_repeat:
            repeated_windows = detect_repeat_windows(merged["A"], win_steps)
            merged["A"], merged["B"], merged["C"], repeat_hits = apply_repeat_variation(
                merged["A"], merged["B"], merged["C"], repeated_windows, win_steps
            )

        melody_starts = {s for s, _, _ in merged["A"]}
        merged["B"], lag_b = apply_support_lag(merged["B"], melody_starts, human_delay_steps, human_lag_ratio)
        merged["C"], lag_c = apply_support_lag(
            merged["C"],
            melody_starts,
            human_delay_steps,
            (human_lag_ratio * 0.25) if mode in {"sad", "lite"} else (human_lag_ratio * 0.75),
        )
        lag_hits = lag_b + lag_c

        if use_pickup_push:
            merged["B"], pickup_b = apply_pickup_push(merged["B"], human_pickup_ratio)
            bass_pickup_ratio = human_pickup_ratio * 0.55
            merged["C"], pickup_c = apply_pickup_push(merged["C"], bass_pickup_ratio)
            pickup_hits = pickup_b + pickup_c

        merged["B"], release_b = apply_human_release(merged["B"], human_release_ratio)
        merged["C"], release_c = apply_human_release(
            merged["C"],
            (human_release_ratio * 0.20) if mode in {"sad", "lite"} else (human_release_ratio * 0.85),
        )
        release_hits = release_b + release_c

        if use_hand:
            merged, hand_drop = apply_hand_constraints(
                merged,
                left_hand_max=3,
                right_hand_max=3,
                hand_max_jump=10,
                hand_min_react_steps=2,
            )
        if mode == "sad":
            merged["A"], lg_a = enforce_legato_floor(merged["A"], min_steps=3, weak_extra=0)
            merged["B"], lg_b = enforce_legato_floor(merged["B"], min_steps=2, weak_extra=0)
            merged["C"], lg_c = enforce_legato_floor(merged["C"], min_steps=2, weak_extra=0)
            legato_hits = lg_a + lg_b + lg_c
    else:
        merged["A"], breath_hits = apply_melody_breath(merged["A"], melody_breath_every, melody_breath_gap)

    mapped_end = (max(n["end_step"] for n in mapped) + 1) if mapped else 1
    merged_end = max((e for v in merged.values() for _, e, _ in v), default=1) + 1
    total_steps = max(mapped_end, merged_end)

    seg_a = intervals_to_segments_limited(merged["A"], total_steps, p.a_max_poly)
    seg_b = intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)
    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    tempo_steps = coarsen_tempo_steps(
        tempo_steps,
        min_gap_steps=(32 if mode == "sad" else (24 if mode == "lite" else 12)),
        min_bpm_delta=(3 if mode == "sad" else (2 if mode == "lite" else 1)),
    )
    if humanize:
        phrase_ranges = build_phrase_ranges(merged["A"])
        tempo_steps = build_rubato_tempo_steps(tempo_steps, phrase_ranges, rubato_depth)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)
    base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = next_script_output_path(out_dir, base, "script_longnote_human_v2")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    style_summary = ", ".join(f"{k}:{v}" for k, v in style_stats.items())
    density_summary = ", ".join(f"w{w:02d}:{d}" for w, d in sorted(density.items())[:16])
    out = [
        f"Title: {base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
        f"Source: {os.path.basename(input_midi)}",
        f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
        f"Info: profile={p.name}, {p.desc}",
        f"Info: melody_breath=every:{melody_breath_every}, gap:{melody_breath_gap}, hits:{breath_hits}",
        (
            "Info: humanize=on, "
            f"mode:{mode}, rubato+/-{rubato_depth}bpm gradual, "
            f"delay_step:{human_delay_steps}, lag_ratio:{human_lag_ratio:.2f}, pickup_ratio:{human_pickup_ratio:.2f}, release_ratio:{human_release_ratio:.2f}, "
            f"hits:lag={lag_hits}, pickup={pickup_hits}, release={release_hits}, repeat={repeat_hits}, hand_drop={hand_drop}, legato={legato_hits}"
            if humanize
            else "Info: humanize=off"
        ),
        f"Info: style_windows={style_summary if mode == 'full' else f'off({mode})'}",
        f"Info: density_windows={density_summary if density_summary else 'n/a'}",
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
    text = "\n".join(out)
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
        "removed": removed,
        "humanize": humanize,
        "human_mode": mode,
        "rubato_depth": rubato_depth,
        "style_stats": style_stats,
        "density_summary": density_summary,
        "human_delay_steps": human_delay_steps,
        "human_lag_ratio": human_lag_ratio,
        "human_pickup_ratio": human_pickup_ratio,
        "human_release_ratio": human_release_ratio,
        "melody_breath_every": melody_breath_every,
        "melody_breath_gap": melody_breath_gap,
        "breath_hits": breath_hits,
        "lag_hits": lag_hits,
        "pickup_hits": pickup_hits,
        "release_hits": release_hits,
        "repeat_hits": repeat_hits,
        "hand_drop": hand_drop,
        "pocket_hits": pocket_hits,
        "legato_hits": legato_hits,
        "play": play,
    }


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(re.escape(safe_base) + r"_analysis_longnote_human_v2_v(\d+)\.md$", re.I)
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_longnote_human_v2_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str]):
    lines = [
        f"# Analysis (Longnote Human V2 Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Longnote Human V2 Script Intent",
        "- preserve sustained melody notes and reduce ornament-like slicing",
        "- keep harmony layers readable without masking long tones",
        "- add gradual rubato, pocket, style windows, repeat variation and hand reachability",
        "- maintain 21-key playability and parser-safe syntax",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="Analyze + profile-select + convert DoMiSo workflow.")
    sub = ap.add_subparsers(dest="cmd")
    ap_an = sub.add_parser("analyze")
    ap_an.add_argument("input_midi")
    ap_an.add_argument("--json", action="store_true")
    ap_cv = sub.add_parser("convert")
    ap_cv.add_argument("input_midi")
    ap_cv.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_cv.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    ap_cv.set_defaults(humanize=True)
    ap_cv.add_argument("--no-humanize", action="store_false", dest="humanize")
    ap_cv.add_argument("--human-mode", default="sad", choices=["sad", "lite", "full"])
    ap_cv.add_argument("--human-delay-steps", type=int, default=None)
    ap_cv.add_argument("--human-lag-ratio", type=float, default=None)
    ap_cv.add_argument("--human-pickup-ratio", type=float, default=None)
    ap_cv.add_argument("--human-release-ratio", type=float, default=None)
    ap_cv.add_argument("--melody-breath-every", type=int, default=None)
    ap_cv.add_argument("--melody-breath-gap", type=int, default=None)
    ap_pl = sub.add_parser("pipeline")
    ap_pl.add_argument("input_midi")
    ap_pl.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--report-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    ap_pl.set_defaults(humanize=True)
    ap_pl.add_argument("--no-humanize", action="store_false", dest="humanize")
    ap_pl.add_argument("--human-mode", default="sad", choices=["sad", "lite", "full"])
    ap_pl.add_argument("--human-delay-steps", type=int, default=None)
    ap_pl.add_argument("--human-lag-ratio", type=float, default=None)
    ap_pl.add_argument("--human-pickup-ratio", type=float, default=None)
    ap_pl.add_argument("--human-release-ratio", type=float, default=None)
    ap_pl.add_argument("--melody-breath-every", type=int, default=None)
    ap_pl.add_argument("--melody-breath-gap", type=int, default=None)
    ap_cp = sub.add_parser("compare")
    ap_cp.add_argument("file_a")
    ap_cp.add_argument("file_b")
    args = ap.parse_args()

    if args.cmd == "analyze":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m)
        out = {"input": args.input_midi, "recommended_profile": p, "reasons": r, "metrics": m}
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else out)
        return
    if args.cmd == "convert":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(
            args.input_midi,
            args.out_dir,
            p,
            humanize=args.humanize,
            human_mode=args.human_mode,
            human_delay_steps=args.human_delay_steps,
            human_lag_ratio=args.human_lag_ratio,
            human_release_ratio=args.human_release_ratio,
            human_pickup_ratio=args.human_pickup_ratio,
            melody_breath_every=args.melody_breath_every,
            melody_breath_gap=args.melody_breath_gap,
        )
        print(f"output={res['output']}")
        print(f"profile={res['profile']}")
        if r:
            print(f"profile_reasons={'; '.join(r)}")
        print(
            "humanize="
            f"{'on' if res['humanize'] else 'off'}, "
            f"mode:{res['human_mode']}, "
            f"delay_step={res['human_delay_steps']}, lag_ratio={res['human_lag_ratio']:.2f}, "
            f"pickup_ratio={res['human_pickup_ratio']:.2f}, release_ratio={res['human_release_ratio']:.2f}, "
            f"melody_breath=every:{res['melody_breath_every']},gap:{res['melody_breath_gap']}, "
            f"hits=breath:{res['breath_hits']},lag:{res['lag_hits']},pickup:{res['pickup_hits']},release:{res['release_hits']},"
            f"pocket:{res['pocket_hits']},repeat:{res['repeat_hits']},hand_drop:{res['hand_drop']},legato:{res['legato_hits']}"
        )
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return
    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(
            args.input_midi,
            args.out_dir,
            p,
            humanize=args.humanize,
            human_mode=args.human_mode,
            human_delay_steps=args.human_delay_steps,
            human_lag_ratio=args.human_lag_ratio,
            human_release_ratio=args.human_release_ratio,
            human_pickup_ratio=args.human_pickup_ratio,
            melody_breath_every=args.melody_breath_every,
            melody_breath_gap=args.melody_breath_gap,
        )
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(report, args.input_midi, m, p, r)
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={p}")
        print(
            "humanize="
            f"{'on' if res['humanize'] else 'off'}, "
            f"mode:{res['human_mode']}, "
            f"delay_step={res['human_delay_steps']}, lag_ratio={res['human_lag_ratio']:.2f}, "
            f"pickup_ratio={res['human_pickup_ratio']:.2f}, release_ratio={res['human_release_ratio']:.2f}, "
            f"melody_breath=every:{res['melody_breath_every']},gap:{res['melody_breath_gap']}, "
            f"hits=breath:{res['breath_hits']},lag:{res['lag_hits']},pickup:{res['pickup_hits']},release:{res['release_hits']},"
            f"pocket:{res['pocket_hits']},repeat:{res['repeat_hits']},hand_drop:{res['hand_drop']},legato:{res['legato_hits']}"
        )
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return
    if args.cmd == "compare":
        pa = evaluate_txt_playability(args.file_a)
        pb = evaluate_txt_playability(args.file_b)
        print(json.dumps({"A": {"path": args.file_a, "playability": pa}, "B": {"path": args.file_b, "playability": pb}}, ensure_ascii=False, indent=2))
        return

    # legacy shortcut
    legacy = argparse.ArgumentParser(description="legacy convert")
    legacy.add_argument("input_midi")
    legacy.add_argument("--out-dir", default=r"d:\domiso\txt")
    legacy.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    legacy.set_defaults(humanize=True)
    legacy.add_argument("--no-humanize", action="store_false", dest="humanize")
    legacy.add_argument("--human-mode", default="sad", choices=["sad", "lite", "full"])
    legacy.add_argument("--human-delay-steps", type=int, default=None)
    legacy.add_argument("--human-lag-ratio", type=float, default=None)
    legacy.add_argument("--human-pickup-ratio", type=float, default=None)
    legacy.add_argument("--human-release-ratio", type=float, default=None)
    legacy.add_argument("--melody-breath-every", type=int, default=None)
    legacy.add_argument("--melody-breath-gap", type=int, default=None)
    l = legacy.parse_args()
    parsed = core.parse_midi(l.input_midi)
    m = analyze_midi(parsed)
    p, _ = recommend_profile(m) if l.profile == "auto" else (l.profile, [])
    res = convert_midi(
        l.input_midi,
        l.out_dir,
        p,
        humanize=l.humanize,
        human_mode=l.human_mode,
        human_delay_steps=l.human_delay_steps,
        human_lag_ratio=l.human_lag_ratio,
        human_release_ratio=l.human_release_ratio,
        human_pickup_ratio=l.human_pickup_ratio,
        melody_breath_every=l.melody_breath_every,
        melody_breath_gap=l.melody_breath_gap,
    )
    print(f"output={res['output']}")
    print(f"profile={res['profile']}")
    print(
        "humanize="
        f"{'on' if res['humanize'] else 'off'}, "
        f"mode:{res['human_mode']}, "
        f"delay_step={res['human_delay_steps']}, lag_ratio={res['human_lag_ratio']:.2f}, "
        f"pickup_ratio={res['human_pickup_ratio']:.2f}, release_ratio={res['human_release_ratio']:.2f}, "
        f"melody_breath=every:{res['melody_breath_every']},gap:{res['melody_breath_gap']}, "
        f"hits=breath:{res['breath_hits']},lag:{res['lag_hits']},pickup:{res['pickup_hits']},release:{res['release_hits']},"
        f"pocket:{res['pocket_hits']},repeat:{res['repeat_hits']},hand_drop:{res['hand_drop']},legato:{res['legato_hits']}"
    )
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")


if __name__ == "__main__":
    main()
