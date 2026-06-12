#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

import midi_to_domiso_dense3layer as core


PLAYABLE_NOTES = {
    48, 50, 52, 53, 55, 57, 59,
    60, 62, 64, 65, 67, 69, 71,
    72, 74, 76, 77, 79, 81, 83,
}
BASE_OFFSETS = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
TOP_CHORD_MIN = 72
ALL_PLAYABLE_NOTES = tuple(sorted(PLAYABLE_NOTES))
SINGLE_NOTE_PLAYABLE = tuple(n for n in ALL_PLAYABLE_NOTES if n < TOP_CHORD_MIN)
STYLE_ARP = "arpeggio"
STYLE_FOLK = "folk_strum"
STYLE_MUTED = "muted_strum"
STYLE_BASS = "bass_strum"
STYLE_LEAD = "lead_mix"
STYLE_SET = {STYLE_ARP, STYLE_FOLK, STYLE_MUTED, STYLE_BASS, STYLE_LEAD}


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
    top_chord_mode: str  # "avoid" | "pad" | "allow"
    chord_pad_min_gap: int
    chord_pad_min_dur: int
    chord_pad_max_dur: int
    chord_pad_melody_limit: int
    chord_pad_b_overlap_max: float
    chord_pad_max_silence: int
    melody_pref_low: int
    melody_pref_high: int
    melody_leap_soft: int


PROFILES: Dict[str, Profile] = {
    "guitar_solo": Profile(
        "guitar_solo", "guitar timbre friendly: melody first, very sparse accompaniment",
        -5, 5, 2.3, False, (0,), 0, "contour", False, 1, 0, False, 2, 88, 1, 1, 1,
        "avoid", 0, 0, 0, 0, 0.0, 0, 60, 71, 6
    ),
    "guitar_balanced": Profile(
        "guitar_balanced", "guitar timbre friendly balanced support with clean mid-low bed",
        -7, 7, 1.9, True, (0, -2, -1, 1, 2), 2, "contour", False, 1, 0, False, 1, 78, 1, 1, 1,
        "pad", 12, 4, 8, 2, 0.35, 20, 60, 71, 6
    ),
    "guitar_dense": Profile(
        "guitar_dense", "guitar timbre friendly dense material with anti-mud limits",
        -8, 8, 1.4, True, (0, -2, -1, 1, 2, 3), 2, "contour", False, 1, 1, False, 1, 74, 1, 1, 1,
        "pad", 8, 3, 8, 3, 0.50, 16, 59, 71, 7
    ),
}


def use_single_note_zone_only(p: Profile) -> bool:
    return p.top_chord_mode in {"avoid", "pad"}


def fold_and_snap_profile(pitch: int, p: Profile) -> Tuple[int, float]:
    folded = pitch
    fold_count = 0
    while folded < core.PLAYABLE_MIN:
        folded += 12
        fold_count += 1
    while folded > core.PLAYABLE_MAX:
        folded -= 12
        fold_count += 1
    candidates = SINGLE_NOTE_PLAYABLE if use_single_note_zone_only(p) else ALL_PLAYABLE_NOTES
    best = min(candidates, key=lambda n: (abs(n - folded), abs(n - pitch), n))
    dist = abs(best - folded) + 0.35 * fold_count
    if use_single_note_zone_only(p) and folded >= TOP_CHORD_MIN:
        # Encourage shifts that naturally stay out of guitar chord-trigger key row.
        dist += 0.25 * (folded - (TOP_CHORD_MIN - 1))
    return best, dist


def evaluate_shift_cost_profile(notes: List[dict], shift: int, top_ids: set, melody_track: int, tpb: int, p: Profile) -> float:
    total = 0.0
    for i, n in enumerate(notes):
        _, dist = fold_and_snap_profile(n["note"] + shift, p)
        dur = n["end"] - n["start"]
        wt = 1.0
        if i in top_ids:
            wt += 0.8
        if n["track"] == melody_track:
            wt += 0.25
        if dur <= max(1, tpb // 6):
            wt *= 0.7
        total += dist * wt
    return total


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
        reasons.append("high density/polyphony -> guitar dense profile with anti-mud limits")
        return "guitar_dense", reasons
    if metrics["tempo0"] >= 145 and metrics["note_count"] >= 650:
        reasons.append("fast and note-rich -> guitar balanced profile for readability")
        return "guitar_balanced", reasons
    if metrics["time_sig"] == "3/4" and metrics["tracks"] <= 2:
        reasons.append("3/4 + few tracks -> guitar solo keeps lines clean")
        return "guitar_solo", reasons
    reasons.append("default guitar-balanced profile")
    return "guitar_balanced", reasons


def choose_base_shift_profile(notes: List[dict], top_ids: set, melody_track: int, tpb: int, p: Profile) -> int:
    best_s, best_c = 0, float("inf")
    for s in range(p.shift_min, p.shift_max + 1):
        c = evaluate_shift_cost_profile(notes, s, top_ids, melody_track, tpb, p) + p.shift_bias * abs(s)
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
                _, dist = fold_and_snap_profile(n["note"] + s, p)
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


def quantile(vals: List[int], q: float) -> float:
    if not vals:
        return 0.0
    arr = sorted(vals)
    idx = int(round((len(arr) - 1) * max(0.0, min(1.0, q))))
    return float(arr[idx])


def summarize_style_windows(styles: List[str]) -> str:
    if not styles:
        return "w00-w00:folk_strum"
    parts = []
    s = 0
    cur = styles[0]
    for i in range(1, len(styles)):
        if styles[i] != cur:
            parts.append((s, i - 1, cur))
            s = i
            cur = styles[i]
    parts.append((s, len(styles) - 1, cur))
    return ", ".join(f"w{a:02d}-w{b:02d}:{name}" for a, b, name in parts)


def build_style_plan(
    mapped_notes: List[dict],
    voices: Dict[str, List[Tuple[int, int, int]]],
    window_steps: int,
    tempo0: int,
) -> Tuple[List[str], str, Dict[str, int]]:
    if not mapped_notes:
        styles = [STYLE_FOLK]
        return styles, summarize_style_windows(styles), {STYLE_FOLK: 1}

    window_steps = max(1, window_steps)
    max_step = max(n["end_step"] for n in mapped_notes)
    cnt = (max_step // window_steps) + 1
    note_cnt = [0] * cnt
    mel_att = [0] * cnt
    bass_att = [0] * cnt
    bass_long = [0] * cnt

    for n in mapped_notes:
        w = min(cnt - 1, n["start_step"] // window_steps)
        note_cnt[w] += 1
    for s, _, _ in voices.get("A", []):
        w = min(cnt - 1, s // window_steps)
        mel_att[w] += 1
    for s, e, _ in voices.get("C", []):
        w = min(cnt - 1, s // window_steps)
        bass_att[w] += 1
        if (e - s) >= 4:
            bass_long[w] += 1

    n_lo = quantile(note_cnt, 0.30)
    n_hi = quantile(note_cnt, 0.70)
    m_med = quantile(mel_att, 0.50)
    b_med = quantile(bass_att, 0.50)
    bl_med = quantile(bass_long, 0.50)

    styles: List[str] = [STYLE_FOLK] * cnt
    for w in range(cnt):
        dense = note_cnt[w] >= max(n_hi, n_lo + 3)
        sparse = note_cnt[w] <= n_lo
        mel_busy = mel_att[w] >= (m_med + 2)
        bass_busy = bass_att[w] >= (b_med + 1)
        bass_anchor = bass_long[w] >= max(1.0, bl_med)

        style = STYLE_FOLK
        if dense and mel_busy:
            style = STYLE_LEAD
        elif dense and (tempo0 >= 138 or bass_busy):
            style = STYLE_MUTED
        elif sparse and mel_busy:
            style = STYLE_ARP
        elif bass_anchor and not mel_busy:
            style = STYLE_BASS
        elif sparse:
            style = STYLE_ARP
        styles[w] = style

    # Remove 1-window jitter.
    for i in range(1, len(styles) - 1):
        if styles[i - 1] == styles[i + 1] and styles[i] != styles[i - 1]:
            styles[i] = styles[i - 1]

    counts = Counter(styles)
    summary = summarize_style_windows(styles)
    return styles, summary, {k: counts.get(k, 0) for k in sorted(STYLE_SET)}


def map_notes_profile(
    notes: List[dict], shifts: List[int], window_ticks: int, tick_per_step: float, p: Profile
) -> Tuple[List[dict], float]:
    mapped = []
    total_dist = 0.0
    for n in notes:
        win = min(len(shifts) - 1, max(0, n["start"] // window_ticks))
        shift = shifts[win]
        pitch, dist = fold_and_snap_profile(n["note"] + shift, p)
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


def degree_from_pitch(pitch: int) -> int | None:
    degree = core.DEGREE_BY_PC.get(pitch % 12)
    return int(degree) if degree is not None else None


def choose_chord_degree(bass_deg: int, next_deg: int | None) -> int:
    if bass_deg == 7:
        # Use G7 only when resolving to tonic soon; otherwise keep dominant G.
        return 7 if next_deg == 1 else 5
    return bass_deg


def meter_to_bar_steps_and_strong(time_sigs: List[Tuple[int, int, int]]) -> Tuple[int, Tuple[int, ...]]:
    if not time_sigs:
        return 16, (0, 8)
    _, num, den = time_sigs[0]
    bar_steps = int(max(1, round(num * (16.0 / den))))
    if (num, den) == (6, 8):
        return 12, (0, 6)
    if (num, den) == (3, 4):
        return 12, (0,)
    if num >= 4:
        half = bar_steps // 2
        return bar_steps, (0, half)
    return bar_steps, (0,)


def next_strong_step(start: int, bar_steps: int, strong_offsets: Tuple[int, ...]) -> int:
    if not strong_offsets:
        return start
    bar = start // bar_steps
    pos = start % bar_steps
    sorted_offsets = tuple(sorted(set(int(x) % bar_steps for x in strong_offsets)))
    for off in sorted_offsets:
        if off >= pos:
            return bar * bar_steps + off
    return (bar + 1) * bar_steps + sorted_offsets[0]


def attack_set(intervals: List[Tuple[int, int, int]]) -> set:
    return {s for s, _, _ in intervals}


def count_attacks_near(attacks: set, step: int, radius: int = 4) -> int:
    if not attacks:
        return 0
    cnt = 0
    for t in range(step - radius, step + radius + 1):
        if t in attacks:
            cnt += 1
    return cnt


def overlap_ratio(intervals: List[Tuple[int, int, int]], s: int, e: int) -> float:
    span = max(1, e - s)
    ov = 0
    for is_, ie, _ in intervals:
        a = max(s, is_)
        b = min(e, ie)
        if b > a:
            ov += (b - a)
    return ov / span


def remap_melody_register(intervals: List[Tuple[int, int, int]], p: Profile) -> List[Tuple[int, int, int]]:
    if not intervals:
        return intervals
    out: List[Tuple[int, int, int]] = []
    prev_pitch = None
    center = (p.melody_pref_low + p.melody_pref_high) / 2.0

    for s, e, pitch in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        cands = []
        for delta in (-24, -12, 0, 12, 24):
            c = pitch + delta
            if c in SINGLE_NOTE_PLAYABLE:
                cands.append(c)
        if not cands:
            # Fallback: keep original if already playable in single-note zone.
            cands = [pitch] if pitch in SINGLE_NOTE_PLAYABLE else [max(min(pitch, 71), 48)]
            cands = [min(SINGLE_NOTE_PLAYABLE, key=lambda x: abs(x - cands[0]))]

        cands_primary = [c for c in cands if p.melody_pref_low <= c <= p.melody_pref_high]
        if cands_primary:
            cands = cands_primary

        best = cands[0]
        best_score = float("inf")
        for c in cands:
            score = 0.0
            score += 0.35 * abs(c - pitch)  # keep contour, but allow octave relocation for guitar fingering
            if c < p.melody_pref_low:
                score += 5.0 + 1.0 * (p.melody_pref_low - c)
            elif c > p.melody_pref_high:
                score += 5.0 + 1.0 * (c - p.melody_pref_high)

            if prev_pitch is None:
                score += 0.6 * abs(c - center)
            else:
                leap = abs(c - prev_pitch)
                score += 1.2 * leap
                if leap > p.melody_leap_soft:
                    score += 1.6 * (leap - p.melody_leap_soft)
                if leap > 12:
                    score += 4.0 + 1.2 * (leap - 12)

            if score < best_score:
                best_score = score
                best = c

        out.append((s, e, best))
        prev_pitch = best

    return out


def build_chord_pads_from_bass(
    bass_intervals: List[Tuple[int, int, int]],
    harmony_intervals: List[Tuple[int, int, int]],
    melody_intervals: List[Tuple[int, int, int]],
    time_sigs: List[Tuple[int, int, int]],
    style_by_window: List[str],
    style_window_steps: int,
    p: Profile,
) -> List[Tuple[int, int, int]]:
    if p.top_chord_mode != "pad" or p.chord_pad_min_gap <= 0:
        return []

    bar_steps, strong_offsets = meter_to_bar_steps_and_strong(time_sigs)
    mel_attacks = attack_set(melody_intervals)
    style_window_steps = max(1, style_window_steps)

    def style_at(step: int) -> str:
        if not style_by_window:
            return STYLE_FOLK
        idx = min(len(style_by_window) - 1, max(0, step // style_window_steps))
        return style_by_window[idx]

    entries: List[Tuple[int, int, int, str]] = []
    for s, e, pitch in sorted(bass_intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        deg = degree_from_pitch(pitch)
        if deg is None:
            continue
        style = style_at(s)
        # Prefer strong-beat trigger points for a more guitar-like comping feel.
        s2 = next_strong_step(s, bar_steps, strong_offsets)
        if style == STYLE_BASS:
            # Typical bass + strum: chord stroke slightly after bass anchor.
            s2 = min(e - 1, s2 + 2)
        if s2 >= e:
            continue
        entries.append((s2, e, deg, style))
        if style == STYLE_MUTED and (e - s2) >= 6:
            # Add a light off-beat stroke for muted strum feel.
            s3 = s2 + 2
            if s3 < e:
                entries.append((s3, e, deg, style))

    pads: List[Tuple[int, int, int]] = []
    last_pad = -10**9
    for i, (s, e, deg, style) in enumerate(entries):
        gap = p.chord_pad_min_gap
        min_dur = p.chord_pad_min_dur
        max_dur = p.chord_pad_max_dur
        mel_limit_base = p.chord_pad_melody_limit
        overlap_base = p.chord_pad_b_overlap_max

        if style == STYLE_ARP:
            gap = max(gap * 2, 16)
            min_dur = max(min_dur, 3)
            max_dur = min(max_dur, 6)
            mel_limit_base = max(0, mel_limit_base - 1)
        elif style == STYLE_FOLK:
            gap = max(gap, 10)
            min_dur = max(min_dur, 4)
            max_dur = max(max_dur, min_dur)
        elif style == STYLE_MUTED:
            gap = max(6, gap - 3)
            min_dur = max(2, min_dur - 1)
            max_dur = min(4, max(max_dur, min_dur))
            mel_limit_base = mel_limit_base + 1
        elif style == STYLE_BASS:
            gap = max(gap, 10)
            min_dur = max(3, min_dur)
            max_dur = min(max_dur, 6)
            mel_limit_base = max(0, mel_limit_base - 1)
        elif style == STYLE_LEAD:
            gap = max(gap * 2, 16)
            min_dur = max(2, min_dur - 1)
            max_dur = min(4, max(max_dur, min_dur))
            mel_limit_base = max(0, mel_limit_base - 1)

        if s - last_pad < gap:
            continue
        force_fill = p.chord_pad_max_silence > 0 and (s - last_pad) >= p.chord_pad_max_silence
        mel_limit = mel_limit_base + (1 if force_fill else 0)
        if count_attacks_near(mel_attacks, s, radius=4) > mel_limit:
            continue
        next_deg = entries[i + 1][2] if i + 1 < len(entries) else None
        chord_deg = choose_chord_degree(deg, next_deg)
        chord_pitch = TOP_CHORD_MIN + BASE_OFFSETS[chord_deg]
        span = e - s
        activity = count_attacks_near(mel_attacks, s, radius=6)
        if activity >= mel_limit_base:
            dur = min_dur
        else:
            dur = max(min_dur, span // 2)
            dur = min(max_dur, dur)
        end = min(e, s + dur)
        if end <= s:
            continue
        overlap_max = overlap_base + (0.2 if force_fill else 0.0)
        if overlap_ratio(harmony_intervals, s, end) > overlap_max:
            continue
        if (not force_fill) and pads and pads[-1][2] == chord_pitch and (s - pads[-1][0]) < (gap * 2):
            # Avoid repeated same-chord pumping in short windows.
            continue
        pads.append((s, end, chord_pitch))
        last_pad = s

    return pads


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


def evaluate_top_chord_usage(path: str):
    text = open(path, "r", encoding="utf-8").read()
    base = 60
    for m in re.finditer(r"(?mi)\b1=([A-G]\d?\d?[#b]?)\b", text):
        maybe = key_to_midi(m.group(1))
        if maybe is not None:
            base = maybe
    total = 0
    top = 0
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
        if tune >= TOP_CHORD_MIN:
            top += 1
    safe = total - top
    return {
        "notes": total,
        "top_chord_zone": top,
        "safe_single_zone": safe,
        "safe_ratio": (safe / total * 100.0) if total else 0.0,
    }


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


def convert_midi(input_midi: str, out_dir: str, profile_name: str):
    p = PROFILES[profile_name]
    parsed = core.parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)
    base_shift = choose_base_shift_profile(notes, top_ids, parsed["melody_track"], tpb, p)
    shifts, win_ticks, changes = choose_dynamic_shifts_profile(notes, top_ids, parsed["melody_track"], tpb, base_shift, p)
    tick_per_step = tpb / 4.0
    style_window_steps = max(1, int(round(win_ticks / tick_per_step)))
    mapped, dist = map_notes_profile(notes, shifts, win_ticks, tick_per_step, p)
    voices, removed = assign_voices_profile(mapped, parsed["melody_track"], parsed["bass_track"], p)
    voices["A"] = remap_melody_register(voices["A"], p)
    styles, style_summary, style_counts = build_style_plan(mapped, voices, style_window_steps, tempos[0][1])
    chord_pads = build_chord_pads_from_bass(
        voices["C"],
        voices["B"],
        voices["A"],
        parsed["time_sigs"],
        styles,
        style_window_steps,
        p,
    )
    if chord_pads:
        voices["B"].extend(chord_pads)
    merged = {k: core.merge_intervals(v) for k, v in voices.items()}
    total_steps = max(n["end_step"] for n in mapped) + 1
    seg_a = intervals_to_segments_limited(merged["A"], total_steps, p.a_max_poly)
    seg_b = intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)
    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)
    base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = next_script_output_path(out_dir, base, "script_guitar")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    out = [
        f"Title: {base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
        f"Source: {os.path.basename(input_midi)}",
        f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
        f"Info: profile={p.name}, {p.desc}",
        f"Info: top_chord_mode={p.top_chord_mode} (single-note mapping prefers lower+middle rows)",
        f"Info: chord_pads_from_bass={len(chord_pads)}",
        f"Info: guitar_style_windows(4 bars): {style_summary}",
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
    top_usage = evaluate_top_chord_usage(out_path)
    return {
        "output": out_path,
        "profile": p.name,
        "notes": len(notes),
        "base_shift": base_shift,
        "changes": changes,
        "summary": summary,
        "dist": round(dist, 2),
        "removed": removed,
        "chord_pads": len(chord_pads),
        "style_summary": style_summary,
        "style_counts": style_counts,
        "play": play,
        "top_usage": top_usage,
    }


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(re.escape(safe_base) + r"_analysis_guitar_v(\d+)\.md$", re.I)
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_guitar_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str], conv: dict | None = None):
    output_lines = []
    if conv:
        output_lines = [
            "",
            "## Output Checks",
            f"- playability: {conv['play']['playable']}/{conv['play']['notes']} ({conv['play']['ratio']:.2f}%)",
            f"- top chord-zone usage: {conv['top_usage']['top_chord_zone']}/{conv['top_usage']['notes']} "
            f"(safe {conv['top_usage']['safe_ratio']:.2f}%)",
            f"- chord pads injected: {conv['chord_pads']}",
            f"- style windows: {conv['style_summary']}",
            f"- style counts: {conv['style_counts']}",
            "",
        ]
    lines = [
        f"# Analysis (Guitar Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Guitar Script Intent",
        "- melody mapping avoids direct top-row chord-trigger substitution",
        "- accompaniment may trigger top-row chord keys from bass anchors (controlled density)",
        "- keep key layout compatible with normal DoMiSo positions",
        "- optimize arrangement for guitar timbre by reducing muddy overlap",
        "- keep melody clear while simplifying accompaniment density",
        "- maintain 21-key playability and parser-safe syntax",
        "",
        *output_lines,
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="Analyze + profile-select + convert DoMiSo guitar-timbre workflow.")
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
        m = analyze_midi(parsed)
        p, r = recommend_profile(m)
        out = {"input": args.input_midi, "recommended_profile": p, "reasons": r, "metrics": m}
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else out)
        return
    if args.cmd == "convert":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, p)
        print(f"output={res['output']}")
        print(f"profile={res['profile']}")
        if r:
            print(f"profile_reasons={'; '.join(r)}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        print(f"chord_pads={res['chord_pads']}")
        print(f"style_windows={res['style_summary']}")
        print(
            f"top_chord_zone_usage={res['top_usage']['top_chord_zone']}/{res['top_usage']['notes']} "
            f"(safe {res['top_usage']['safe_ratio']:.2f}%)"
        )
        return
    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, p)
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(report, args.input_midi, m, p, r, res)
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={p}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        print(f"chord_pads={res['chord_pads']}")
        print(f"style_windows={res['style_summary']}")
        print(
            f"top_chord_zone_usage={res['top_usage']['top_chord_zone']}/{res['top_usage']['notes']} "
            f"(safe {res['top_usage']['safe_ratio']:.2f}%)"
        )
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
    l = legacy.parse_args()
    parsed = core.parse_midi(l.input_midi)
    m = analyze_midi(parsed)
    p, _ = recommend_profile(m) if l.profile == "auto" else (l.profile, [])
    res = convert_midi(l.input_midi, l.out_dir, p)
    print(f"output={res['output']}")
    print(f"profile={res['profile']}")
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
    print(f"chord_pads={res['chord_pads']}")
    print(f"style_windows={res['style_summary']}")
    print(
        f"top_chord_zone_usage={res['top_usage']['top_chord_zone']}/{res['top_usage']['notes']} "
        f"(safe {res['top_usage']['safe_ratio']:.2f}%)"
    )


if __name__ == "__main__":
    main()
