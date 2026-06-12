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
    a_max_poly: int
    b_max_poly: int
    c_max_poly: int
    melody_min_steps: int
    b_keep_strong: int
    b_keep_weak: int
    b_weak_delay_steps: int
    breath_every_steps: int
    breath_gap_steps: int
    breath_jump_trigger: int
    human_delay_steps: int
    human_support_lag_ratio: float
    human_strum_ratio: float
    human_release_ratio: float


PROFILES: Dict[str, Profile] = {
    "literal_arranged_soft": Profile(
        "literal_arranged_soft",
        "literal-based adaptation: melody-first, restrained harmony, phrase breathing",
        -12,
        12,
        0.25,
        False,
        (0,),
        0,
        2,
        8,
        2,
        2,
        2,
        0,
        1,
        24,
        1,
        7,
        1,
        0.42,
        0.30,
        0.24,
    ),
    "literal_arranged_balanced": Profile(
        "literal_arranged_balanced",
        "literal-based adaptation: keep identity, cleaner layers, less mechanical",
        -12,
        12,
        0.15,
        True,
        (0, -2, -1, 1, 2),
        1,
        2,
        12,
        3,
        2,
        2,
        0,
        1,
        20,
        1,
        6,
        1,
        0.34,
        0.24,
        0.20,
    ),
    "literal_arranged_dense": Profile(
        "literal_arranged_dense",
        "literal-based adaptation for dense sources: preserve hooks with anti-mud pruning",
        -12,
        12,
        0.10,
        True,
        (0, -2, -1, 1, 2),
        1,
        2,
        16,
        3,
        2,
        2,
        0,
        1,
        18,
        1,
        6,
        1,
        0.24,
        0.18,
        0.16,
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
    if metrics["max_poly"] >= 7 or metrics["bar_density_p90"] >= 24:
        reasons.append("high polyphony/density -> literal_arranged_dense")
        return "literal_arranged_dense", reasons
    if metrics["tempo0"] >= 145:
        reasons.append("faster song -> literal_arranged_balanced")
        return "literal_arranged_balanced", reasons
    reasons.append("default literal_arranged_soft")
    return "literal_arranged_soft", reasons


def choose_base_shift_profile(notes: List[dict], top_ids: set, melody_track: int, tpb: int, p: Profile) -> int:
    best_s, best_c = 0, float("inf")
    for s in range(p.shift_min, p.shift_max + 1):
        c = core.evaluate_shift_cost(notes, s, top_ids, melody_track, tpb) + p.shift_bias * abs(s)
        if c < best_c:
            best_s, best_c = s, c
    return best_s


def choose_dynamic_shifts_profile(
    notes: List[dict], top_ids: set, melody_track: int, tpb: int, base: int, p: Profile
):
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
                cost = pc + local[w][s] + (2.0 if s != ps else 0.0) + 0.2 * abs(s - ps)
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
        if max_poly > 0 and len(pitches) > max_poly:
            # Keep low/high context in C/A, full mid bed in B via higher caps.
            if max_poly <= 4:
                half = max_poly // 2
                pitches = pitches[:half] + pitches[-(max_poly - half):]
            else:
                pitches = pitches[:max_poly]
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


def merge_intervals_strict(intervals: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    by_pitch = defaultdict(list)
    for s, e, p in intervals:
        if e <= s:
            continue
        by_pitch[p].append((s, e))

    merged = []
    for pitch, spans in by_pitch.items():
        spans.sort()
        cur_s, cur_e = spans[0]
        for s, e in spans[1:]:
            if s <= cur_e:
                cur_e = max(cur_e, e)
            else:
                merged.append((cur_s, cur_e, pitch))
                cur_s, cur_e = s, e
        merged.append((cur_s, cur_e, pitch))
    merged.sort(key=lambda x: (x[0], x[2], x[1]))
    return merged


def choose_melody_note(arr: List[dict], prev_a: int | None, melody_track: int) -> dict:
    top_start = max(0, len(arr) - 4)
    candidates = arr[top_start:]
    if not candidates:
        return arr[-1]

    def score(n: dict) -> float:
        s = 0.0
        s += 2.2 if n["track"] == melody_track else 0.0
        s += 0.30 * min(8, n["dur_steps"])
        s += 0.015 * n["vel"]
        # Keep a high-register singing line unless melody-track evidence says otherwise.
        s += 0.05 * n["pitch"]
        if prev_a is not None:
            jump = abs(n["pitch"] - prev_a)
            s -= 0.22 * jump
            if jump > 10:
                s -= 1.4
        return s

    return max(candidates, key=score)


def assign_voices_literal_arranged(mapped_notes: List[dict], p: Profile, melody_track: int):
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)

    voices = {"A": [], "B": [], "C": []}
    prev_a = None
    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda x: x["pitch"])
        if not arr:
            continue

        # Melody: follow melody-track evidence first, then keep contour continuity.
        mel = choose_melody_note(arr, prev_a, melody_track)
        a_end = max(mel["end_step"], step + p.melody_min_steps)
        voices["A"].append((step, a_end, mel["pitch"]))
        prev_a = mel["pitch"]

        # Bass: always keep the lowest foundation.
        lo = arr[0]
        voices["C"].append((step, max(lo["end_step"], step + 2), lo["pitch"]))

        # Middle harmony: keep structural notes only, delay weak-beat hits a bit.
        mids = [n for n in arr if n is not mel and n is not lo]
        if not mids:
            continue
        strong = (step % 4) == 0
        weak = (step % 2) == 0 and not strong
        keep = p.b_keep_strong if strong else (p.b_keep_weak if weak else 0)
        if keep <= 0:
            continue
        mids_sorted = sorted(mids, key=lambda n: (n["dur_steps"], -n["vel"], n["pitch"]), reverse=True)
        for n in mids_sorted[:keep]:
            start = step
            if weak and p.b_weak_delay_steps > 0 and n["end_step"] - step > p.b_weak_delay_steps:
                start = step + p.b_weak_delay_steps
            end = max(n["end_step"], start + 1)
            if end > start:
                voices["B"].append((start, end, n["pitch"]))

    return voices, 0


def prune_melody_micro_fragments(intervals: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    out: List[Tuple[int, int, int]] = []
    for s, e, p in intervals:
        d = e - s
        if d <= 1 and (s % 4) != 0:
            continue
        out.append((s, e, p))
    return out


def apply_breath_points(intervals: List[Tuple[int, int, int]], p: Profile) -> List[Tuple[int, int, int]]:
    if not intervals:
        return intervals
    arr = sorted(intervals, key=lambda x: (x[0], x[1], x[2]))
    out: List[Tuple[int, int, int]] = []
    phrase_steps = 0
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
            if jump >= p.breath_jump_trigger and ns <= e:
                cut = max(cut, p.breath_gap_steps)
            if phrase_steps >= p.breath_every_steps and ns <= e:
                cut = max(cut, p.breath_gap_steps)

        new_e = e
        if cut > 0:
            new_e = max(s + 1, e - cut)
            phrase_steps = 0
        out.append((s, new_e, pitch))

    return out


def normalize_ratio(v: float) -> float:
    return max(0.0, min(1.0, float(v)))


def normalize_micro_delay(steps: int, ratio: float) -> Tuple[int, float]:
    s = max(0, int(steps))
    r = normalize_ratio(ratio)
    return s, r


def hash_gate(step: int, pitch: int, ratio: float, salt: int = 0) -> bool:
    if ratio <= 0.0:
        return False
    # Deterministic hash: stable output across runs for the same MIDI.
    h = ((step * 1315423911) ^ (pitch * 2654435761) ^ salt) & 0xFFFFFFFF
    return (h % 1000) < int(ratio * 1000.0)


def apply_support_lag(
    intervals: List[Tuple[int, int, int]],
    melody_starts: set,
    delay_steps: int,
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    if delay_steps <= 0 or ratio <= 0.0:
        return intervals, 0

    out: List[Tuple[int, int, int]] = []
    delayed = 0
    for s, e, pitch in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        dur = e - s
        if s not in melody_starts or dur < 3:
            out.append((s, e, pitch))
            continue
        local_ratio = ratio * (0.70 if (s % 4) == 0 else 1.00)
        if not hash_gate(s, pitch, local_ratio, salt=0xA341316C):
            out.append((s, e, pitch))
            continue
        ns = s + delay_steps
        ne = max(ns + 1, e)
        out.append((ns, ne, pitch))
        delayed += 1
    return merge_intervals_strict(out), delayed


def apply_human_strum(
    intervals: List[Tuple[int, int, int]],
    delay_steps: int,
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    if delay_steps <= 0 or ratio <= 0.0:
        return intervals, 0

    by_start = defaultdict(list)
    for s, e, pitch in intervals:
        if e > s:
            by_start[s].append((s, e, pitch))

    out: List[Tuple[int, int, int]] = []
    delayed = 0
    for step in sorted(by_start):
        grp = sorted(by_start[step], key=lambda x: x[2])
        if len(grp) <= 1:
            out.extend(grp)
            continue
        for idx, (s, e, pitch) in enumerate(grp):
            dur = e - s
            if idx == 0 or dur < 2:
                out.append((s, e, pitch))
                continue
            local_ratio = ratio * min(1.0, 0.75 + 0.10 * idx)
            if not hash_gate(s, pitch, local_ratio, salt=0x9E3779B9):
                out.append((s, e, pitch))
                continue
            ns = s + delay_steps
            ne = max(ns + 1, e)
            out.append((ns, ne, pitch))
            delayed += 1

    return merge_intervals_strict(out), delayed


def apply_human_release(
    intervals: List[Tuple[int, int, int]],
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    if ratio <= 0.0:
        return intervals, 0

    out: List[Tuple[int, int, int]] = []
    cut = 0
    for s, e, pitch in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        dur = e - s
        weak = (s % 4) != 0
        if weak and dur >= 4 and hash_gate(s, pitch, ratio, salt=0x7F4A7C15):
            ne = max(s + 1, e - 1)
            if ne < e:
                out.append((s, ne, pitch))
                cut += 1
                continue
        out.append((s, e, pitch))
    return merge_intervals_strict(out), cut


def apply_micro_delay(
    intervals: List[Tuple[int, int, int]],
    delay_steps: int,
    ratio: float,
) -> Tuple[List[Tuple[int, int, int]], int]:
    if not intervals:
        return intervals, 0
    if delay_steps <= 0 or ratio <= 0.0:
        return intervals, 0

    start_counts = Counter(s for s, _, _ in intervals)
    out: List[Tuple[int, int, int]] = []
    delayed = 0
    for s, e, pitch in sorted(intervals, key=lambda x: (x[0], x[2], x[1])):
        if e <= s:
            continue
        strong = (s % 4) == 0
        dur = e - s
        # Humanized key-lag should be subtle: only chord attacks and only on longer notes.
        if strong or dur < 3 or start_counts[s] < 2 or not hash_gate(s, pitch, ratio, salt=0xC2B2AE35):
            out.append((s, e, pitch))
            continue
        ns = s + delay_steps
        # Attack-only delay: keep original release as much as possible.
        ne = max(ns + 1, e)
        out.append((ns, ne, pitch))
        delayed += 1

    return merge_intervals_strict(out), delayed


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
    micro_delay_steps: int = 1,
    micro_delay_ratio: float = 0.05,
    humanize: bool = True,
    human_delay_steps: int | None = None,
    human_support_ratio: float | None = None,
    human_strum_ratio: float | None = None,
    human_release_ratio: float | None = None,
):
    p = PROFILES[profile_name]
    micro_delay_steps, micro_delay_ratio = normalize_micro_delay(micro_delay_steps, micro_delay_ratio)
    human_delay_steps = p.human_delay_steps if human_delay_steps is None else max(0, int(human_delay_steps))
    human_support_ratio = normalize_ratio(p.human_support_lag_ratio if human_support_ratio is None else human_support_ratio)
    human_strum_ratio = normalize_ratio(p.human_strum_ratio if human_strum_ratio is None else human_strum_ratio)
    human_release_ratio = normalize_ratio(p.human_release_ratio if human_release_ratio is None else human_release_ratio)
    parsed = core.parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)

    base_shift = choose_base_shift_profile(notes, top_ids, parsed["melody_track"], tpb, p)
    shifts, win_ticks, changes = choose_dynamic_shifts_profile(notes, top_ids, parsed["melody_track"], tpb, base_shift, p)
    tick_per_step = tpb / 4.0
    mapped, dist = core.map_notes(notes, shifts, win_ticks, tick_per_step)

    voices, removed = assign_voices_literal_arranged(mapped, p, parsed["melody_track"])
    merged = {k: merge_intervals_strict(v) for k, v in voices.items()}
    merged["A"] = merge_intervals_strict(
        apply_breath_points(
            prune_melody_micro_fragments(merged["A"]),
            p,
        )
    )
    human_support_hits = 0
    human_strum_hits = 0
    human_release_hits = 0
    if humanize:
        melody_starts = {s for s, _, _ in merged["A"]}
        merged["B"], lag_b = apply_support_lag(merged["B"], melody_starts, human_delay_steps, human_support_ratio)
        merged["C"], lag_c = apply_support_lag(merged["C"], melody_starts, human_delay_steps, human_support_ratio * 0.70)
        human_support_hits = lag_b + lag_c

        merged["B"], strum_b = apply_human_strum(merged["B"], human_delay_steps, human_strum_ratio)
        merged["C"], strum_c = apply_human_strum(merged["C"], human_delay_steps, human_strum_ratio * 0.40)
        human_strum_hits = strum_b + strum_c

        merged["B"], rel_b = apply_human_release(merged["B"], human_release_ratio)
        merged["C"], rel_c = apply_human_release(merged["C"], human_release_ratio * 0.85)
        human_release_hits = rel_b + rel_c

    delayed_b = 0
    delayed_c = 0
    if micro_delay_steps > 0 and micro_delay_ratio > 0.0:
        merged["B"], delayed_b = apply_micro_delay(merged["B"], micro_delay_steps, micro_delay_ratio)
        merged["C"], delayed_c = apply_micro_delay(merged["C"], micro_delay_steps, micro_delay_ratio)

    mapped_end = (max(n["end_step"] for n in mapped) + 1) if mapped else 1
    merged_end = max((e for v in merged.values() for _, e, _ in v), default=1) + 1
    total_steps = max(mapped_end, merged_end)

    seg_a = intervals_to_segments_limited(merged["A"], total_steps, p.a_max_poly)
    seg_b = intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)

    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)

    base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = next_script_output_path(out_dir, base, "script_literal_arranged")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    out = [
        f"Title: {base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
        f"Source: {os.path.basename(input_midi)}",
        f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
        f"Info: profile={p.name}, {p.desc}",
        f"Info: phrasing=melody_min_steps:{p.melody_min_steps}, breath_every:{p.breath_every_steps}, breath_gap:{p.breath_gap_steps}",
        (
            "Info: humanize=on, "
            f"delay_step:{human_delay_steps}, support_ratio:{human_support_ratio:.2f}, strum_ratio:{human_strum_ratio:.2f}, release_ratio:{human_release_ratio:.2f}, "
            f"hits:support={human_support_hits}, strum={human_strum_hits}, release={human_release_hits}"
            if humanize
            else "Info: humanize=off"
        ),
        (
            f"Info: micro_delay=voices(B,C), attack-only, step+{micro_delay_steps}, ratio={micro_delay_ratio:.2f}, delayed={delayed_b + delayed_c}"
            if micro_delay_steps > 0 and micro_delay_ratio > 0.0
            else "Info: micro_delay=off"
        ),
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
        "human_delay_steps": human_delay_steps,
        "human_support_ratio": human_support_ratio,
        "human_strum_ratio": human_strum_ratio,
        "human_release_ratio": human_release_ratio,
        "human_support_hits": human_support_hits,
        "human_strum_hits": human_strum_hits,
        "human_release_hits": human_release_hits,
        "micro_delay_steps": micro_delay_steps,
        "micro_delay_ratio": micro_delay_ratio,
        "micro_delay_hits": delayed_b + delayed_c,
        "play": play,
    }


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(re.escape(safe_base) + r"_analysis_literal_arranged_v(\d+)\.md$", re.I)
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_literal_arranged_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str]):
    lines = [
        f"# Analysis (Literal Arranged Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Literal Arranged Intent",
        "- keep literal-style source identity as baseline",
        "- add light musical arrangement: phrase continuity + breathing + anti-mud harmony",
        "- avoid over-ornament and keep the melody clearly recognizable",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="Analyze + profile-select + literal-arranged DoMiSo conversion workflow.")
    sub = ap.add_subparsers(dest="cmd")
    ap_an = sub.add_parser("analyze")
    ap_an.add_argument("input_midi")
    ap_an.add_argument("--json", action="store_true")
    ap_cv = sub.add_parser("convert")
    ap_cv.add_argument("input_midi")
    ap_cv.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_cv.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    ap_cv.add_argument("--micro-delay-steps", type=int, default=1)
    ap_cv.add_argument("--micro-delay-ratio", type=float, default=0.05)
    ap_cv.set_defaults(humanize=True)
    ap_cv.add_argument("--no-humanize", action="store_false", dest="humanize")
    ap_cv.add_argument("--human-delay-steps", type=int, default=None)
    ap_cv.add_argument("--human-support-ratio", type=float, default=None)
    ap_cv.add_argument("--human-strum-ratio", type=float, default=None)
    ap_cv.add_argument("--human-release-ratio", type=float, default=None)
    ap_pl = sub.add_parser("pipeline")
    ap_pl.add_argument("input_midi")
    ap_pl.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--report-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    ap_pl.add_argument("--micro-delay-steps", type=int, default=1)
    ap_pl.add_argument("--micro-delay-ratio", type=float, default=0.05)
    ap_pl.set_defaults(humanize=True)
    ap_pl.add_argument("--no-humanize", action="store_false", dest="humanize")
    ap_pl.add_argument("--human-delay-steps", type=int, default=None)
    ap_pl.add_argument("--human-support-ratio", type=float, default=None)
    ap_pl.add_argument("--human-strum-ratio", type=float, default=None)
    ap_pl.add_argument("--human-release-ratio", type=float, default=None)
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
            micro_delay_steps=args.micro_delay_steps,
            micro_delay_ratio=args.micro_delay_ratio,
            humanize=args.humanize,
            human_delay_steps=args.human_delay_steps,
            human_support_ratio=args.human_support_ratio,
            human_strum_ratio=args.human_strum_ratio,
            human_release_ratio=args.human_release_ratio,
        )
        print(f"output={res['output']}")
        print(f"profile={res['profile']}")
        if r:
            print(f"profile_reasons={'; '.join(r)}")
        print(
            f"micro_delay=step+{res['micro_delay_steps']}, ratio={res['micro_delay_ratio']:.2f}, hits={res['micro_delay_hits']}"
        )
        print(
            "humanize="
            f"{'on' if res['humanize'] else 'off'}, "
            f"delay_step={res['human_delay_steps']}, support_ratio={res['human_support_ratio']:.2f}, "
            f"strum_ratio={res['human_strum_ratio']:.2f}, release_ratio={res['human_release_ratio']:.2f}, "
            f"hits=support:{res['human_support_hits']},strum:{res['human_strum_hits']},release:{res['human_release_hits']}"
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
            micro_delay_steps=args.micro_delay_steps,
            micro_delay_ratio=args.micro_delay_ratio,
            humanize=args.humanize,
            human_delay_steps=args.human_delay_steps,
            human_support_ratio=args.human_support_ratio,
            human_strum_ratio=args.human_strum_ratio,
            human_release_ratio=args.human_release_ratio,
        )
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(report, args.input_midi, m, p, r)
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={p}")
        print(
            f"micro_delay=step+{res['micro_delay_steps']}, ratio={res['micro_delay_ratio']:.2f}, hits={res['micro_delay_hits']}"
        )
        print(
            "humanize="
            f"{'on' if res['humanize'] else 'off'}, "
            f"delay_step={res['human_delay_steps']}, support_ratio={res['human_support_ratio']:.2f}, "
            f"strum_ratio={res['human_strum_ratio']:.2f}, release_ratio={res['human_release_ratio']:.2f}, "
            f"hits=support:{res['human_support_hits']},strum:{res['human_strum_hits']},release:{res['human_release_hits']}"
        )
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "compare":
        pa = evaluate_txt_playability(args.file_a)
        pb = evaluate_txt_playability(args.file_b)
        print(json.dumps({"A": {"path": args.file_a, "playability": pa}, "B": {"path": args.file_b, "playability": pb}}, ensure_ascii=False, indent=2))
        return

    legacy = argparse.ArgumentParser(description="legacy literal-arranged convert")
    legacy.add_argument("input_midi")
    legacy.add_argument("--out-dir", default=r"d:\domiso\txt")
    legacy.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    legacy.add_argument("--micro-delay-steps", type=int, default=1)
    legacy.add_argument("--micro-delay-ratio", type=float, default=0.05)
    legacy.set_defaults(humanize=True)
    legacy.add_argument("--no-humanize", action="store_false", dest="humanize")
    legacy.add_argument("--human-delay-steps", type=int, default=None)
    legacy.add_argument("--human-support-ratio", type=float, default=None)
    legacy.add_argument("--human-strum-ratio", type=float, default=None)
    legacy.add_argument("--human-release-ratio", type=float, default=None)
    l = legacy.parse_args()
    parsed = core.parse_midi(l.input_midi)
    m = analyze_midi(parsed)
    p, _ = recommend_profile(m) if l.profile == "auto" else (l.profile, [])
    res = convert_midi(
        l.input_midi,
        l.out_dir,
        p,
        micro_delay_steps=l.micro_delay_steps,
        micro_delay_ratio=l.micro_delay_ratio,
        humanize=l.humanize,
        human_delay_steps=l.human_delay_steps,
        human_support_ratio=l.human_support_ratio,
        human_strum_ratio=l.human_strum_ratio,
        human_release_ratio=l.human_release_ratio,
    )
    print(f"output={res['output']}")
    print(f"profile={res['profile']}")
    print(
        f"micro_delay=step+{res['micro_delay_steps']}, ratio={res['micro_delay_ratio']:.2f}, hits={res['micro_delay_hits']}"
    )
    print(
        "humanize="
        f"{'on' if res['humanize'] else 'off'}, "
        f"delay_step={res['human_delay_steps']}, support_ratio={res['human_support_ratio']:.2f}, "
        f"strum_ratio={res['human_strum_ratio']:.2f}, release_ratio={res['human_release_ratio']:.2f}, "
        f"hits=support:{res['human_support_hits']},strum:{res['human_strum_hits']},release:{res['human_release_hits']}"
    )
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")


if __name__ == "__main__":
    main()
