#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Tuple

import mido


PLAYABLE_MIN = 48  # C3
PLAYABLE_MAX = 83  # B5
PLAYABLE_PCS = (0, 2, 4, 5, 7, 9, 11)
DEGREE_BY_PC = {0: "1", 2: "2", 4: "3", 5: "4", 7: "5", 9: "6", 11: "7"}
PLAYABLE_NOTES = [
    p
    for p in range(PLAYABLE_MIN, PLAYABLE_MAX + 1)
    if (p % 12) in PLAYABLE_PCS
]
CHUNK_SUFFIX = [
    (16, "---"),  # 4 beats
    (12, "--"),   # 3 beats
    (8, "-"),     # 2 beats
    (4, ""),      # 1 beat
    (3, "/."),    # 0.75 beat
    (2, "/"),     # 0.5 beat
    (1, "//"),    # 0.25 beat
]


def parse_midi(path: str):
    try:
        mid = mido.MidiFile(path)
    except OSError as exc:
        # Some downloaded MIDIs contain out-of-range data bytes. Retry in clip
        # mode so the generator can still recover usable note/meta events.
        if "data byte must be in range 0..127" not in str(exc):
            raise
        print(
            f"[warn] malformed midi detected, retrying with clip=True: {path}",
            file=sys.stderr,
        )
        mid = mido.MidiFile(path, clip=True)
    tpb = mid.ticks_per_beat

    notes: List[dict] = []
    tempos: List[Tuple[int, float]] = []
    time_sigs: List[Tuple[int, int, int]] = []
    key_sigs: List[Tuple[int, str]] = []
    track_pitches: Dict[int, List[int]] = defaultdict(list)
    max_tick = 0

    for track_idx, track in enumerate(mid.tracks):
        abs_tick = 0
        active: Dict[Tuple[int, int], List[Tuple[int, int]]] = defaultdict(list)

        for msg in track:
            abs_tick += msg.time
            max_tick = max(max_tick, abs_tick)

            if msg.is_meta:
                if msg.type == "set_tempo":
                    tempos.append((abs_tick, mido.tempo2bpm(msg.tempo)))
                elif msg.type == "time_signature":
                    time_sigs.append((abs_tick, msg.numerator, msg.denominator))
                elif msg.type == "key_signature":
                    key_sigs.append((abs_tick, msg.key))
                continue

            if msg.type == "note_on" and msg.velocity > 0:
                active[(msg.channel, msg.note)].append((abs_tick, msg.velocity))
                continue

            if msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                key = (msg.channel, msg.note)
                if active[key]:
                    start_tick, velocity = active[key].pop()
                    end_tick = max(abs_tick, start_tick + 1)
                    notes.append(
                        {
                            "start": start_tick,
                            "end": end_tick,
                            "note": msg.note,
                            "vel": velocity,
                            "track": track_idx,
                        }
                    )
                    track_pitches[track_idx].append(msg.note)

        for (_, note), stacks in active.items():
            for start_tick, velocity in stacks:
                end_tick = max(abs_tick, start_tick + max(1, tpb // 2))
                max_tick = max(max_tick, end_tick)
                notes.append(
                    {
                        "start": start_tick,
                        "end": end_tick,
                        "note": note,
                        "vel": velocity,
                        "track": track_idx,
                    }
                )
                track_pitches[track_idx].append(note)

    def dedupe(items: Iterable[Tuple]) -> List[Tuple]:
        merged = {}
        for item in items:
            merged[item[0]] = item
        return [merged[t] for t in sorted(merged)]

    tempos = dedupe(tempos)
    if not tempos:
        tempos = [(0, 120.0)]
    if tempos[0][0] != 0:
        tempos.insert(0, (0, tempos[0][1]))

    time_sigs = dedupe(time_sigs)
    if not time_sigs:
        time_sigs = [(0, 4, 4)]
    if time_sigs[0][0] != 0:
        time_sigs.insert(0, (0, 4, 4))

    key_sigs = dedupe(key_sigs)

    if not notes:
        raise RuntimeError("No note events found in MIDI.")

    track_medians = {}
    for track_idx in set(n["track"] for n in notes):
        pitches = track_pitches.get(track_idx, [])
        track_medians[track_idx] = statistics.median(pitches) if pitches else 60

    melody_track = max(track_medians, key=lambda k: track_medians[k])
    bass_track = min(track_medians, key=lambda k: track_medians[k])

    return {
        "tpb": tpb,
        "notes": notes,
        "tempos": tempos,
        "time_sigs": time_sigs,
        "key_sigs": key_sigs,
        "max_tick": max_tick,
        "melody_track": melody_track,
        "bass_track": bass_track,
        "track_medians": track_medians,
    }


def clean_tempos(tempos: List[Tuple[int, float]], tpb: int) -> List[Tuple[int, int]]:
    if not tempos:
        return [(0, 120)]

    cleaned: List[Tuple[int, float]] = [tempos[0]]
    for tick, bpm in tempos[1:]:
        prev_tick, prev_bpm = cleaned[-1]
        dt = tick - prev_tick
        if (bpm < 35.0 or bpm > 220.0) and dt < max(1, int(0.5 * tpb)):
            continue
        if abs(bpm - prev_bpm) < 2.0:
            continue
        if dt < tpb:
            continue
        cleaned.append((tick, bpm))

    normalized: List[Tuple[int, int]] = []
    for tick, bpm in cleaned:
        bpm_i = int(round(bpm))
        bpm_i = max(20, min(480, bpm_i))
        if normalized and normalized[-1][1] == bpm_i:
            continue
        normalized.append((tick, bpm_i))

    if normalized[0][0] != 0:
        normalized.insert(0, (0, normalized[0][1]))
    return normalized


def fold_and_snap(pitch: int) -> Tuple[int, float]:
    folded = pitch
    fold_count = 0
    while folded < PLAYABLE_MIN:
        folded += 12
        fold_count += 1
    while folded > PLAYABLE_MAX:
        folded -= 12
        fold_count += 1

    best = min(PLAYABLE_NOTES, key=lambda p: (abs(p - folded), abs(p - pitch), p))
    dist = abs(best - folded) + 0.35 * fold_count
    return best, dist


def build_top_ids(notes: List[dict]) -> set:
    by_start = defaultdict(list)
    for i, n in enumerate(notes):
        by_start[n["start"]].append((n["note"], i))
    top_ids = set()
    for arr in by_start.values():
        top_ids.add(max(arr, key=lambda x: x[0])[1])
    return top_ids


def evaluate_shift_cost(
    notes: List[dict], shift: int, top_ids: set, melody_track: int, tpb: int
) -> float:
    total = 0.0
    for i, n in enumerate(notes):
        _, dist = fold_and_snap(n["note"] + shift)
        dur = n["end"] - n["start"]
        weight = 1.0
        if i in top_ids:
            weight += 0.8
        if n["track"] == melody_track:
            weight += 0.25
        if dur <= max(1, tpb // 6):
            weight *= 0.7
        total += dist * weight
    return total


def choose_base_shift(notes: List[dict], top_ids: set, melody_track: int, tpb: int) -> int:
    best_shift = 0
    best_cost = float("inf")
    for shift in range(-12, 13):
        cost = evaluate_shift_cost(notes, shift, top_ids, melody_track, tpb)
        if cost < best_cost:
            best_cost = cost
            best_shift = shift
    return best_shift


def choose_dynamic_shifts(
    notes: List[dict], top_ids: set, melody_track: int, tpb: int, base_shift: int
) -> Tuple[List[int], int, int]:
    window_ticks = max(1, tpb * 16)  # 4 bars in 4/4
    max_window = max(n["start"] // window_ticks for n in notes)
    window_count = max_window + 1

    candidates = sorted(
        {s for s in (base_shift, base_shift - 2, base_shift + 1, base_shift + 3, 0) if -12 <= s <= 12}
    )
    if not candidates:
        candidates = [base_shift]

    notes_by_window = defaultdict(list)
    for i, n in enumerate(notes):
        notes_by_window[n["start"] // window_ticks].append((i, n))

    local_costs: List[Dict[int, float]] = []
    for w in range(window_count):
        entries = notes_by_window.get(w, [])
        arr = [n for _, n in entries]
        ids = {i for i, _ in entries if i in top_ids}
        cost_map = {}
        for s in candidates:
            if arr:
                # Use local top-note bias where available.
                local_top = set(range(len(arr)))
                if ids:
                    local_top = {j for j, (gi, _) in enumerate(entries) if gi in ids}
                converted_ids = local_top
                pseudo_notes = arr
                total = 0.0
                for j, note in enumerate(pseudo_notes):
                    _, dist = fold_and_snap(note["note"] + s)
                    dur = note["end"] - note["start"]
                    weight = 1.0
                    if j in converted_ids:
                        weight += 0.8
                    if note["track"] == melody_track:
                        weight += 0.25
                    if dur <= max(1, tpb // 6):
                        weight *= 0.7
                    total += dist * weight
                cost_map[s] = total
            else:
                cost_map[s] = 0.0
        local_costs.append(cost_map)

    dp: Dict[Tuple[int, int], float] = {}
    backtrace: List[Dict[Tuple[int, int], Tuple[int, int] | None]] = []

    first_back = {}
    for s in candidates:
        dp[(s, 0)] = local_costs[0][s]
        first_back[(s, 0)] = None
    backtrace.append(first_back)

    for w in range(1, window_count):
        next_dp: Dict[Tuple[int, int], float] = {}
        next_back: Dict[Tuple[int, int], Tuple[int, int]] = {}
        for s in candidates:
            lc = local_costs[w][s]
            for (prev_s, changes), prev_cost in dp.items():
                new_changes = changes + (1 if s != prev_s else 0)
                if new_changes > 2:
                    continue
                switch_penalty = (2.8 if s != prev_s else 0.0) + 0.3 * abs(s - prev_s)
                total = prev_cost + lc + switch_penalty
                key = (s, new_changes)
                if key not in next_dp or total < next_dp[key]:
                    next_dp[key] = total
                    next_back[key] = (prev_s, changes)
        if not next_dp:
            # Fallback to flat base shift when constraints are too tight.
            for changes in range(0, 3):
                key = (base_shift, changes)
                if key in dp:
                    next_dp = {key: dp[key]}
                    next_back = {key: key}
                    break
        dp = next_dp
        backtrace.append(next_back)

    best_state = min(dp, key=lambda k: dp[k])
    shifts = [base_shift] * window_count
    state = best_state
    for w in range(window_count - 1, -1, -1):
        shifts[w] = state[0]
        prev_state = backtrace[w].get(state)
        if prev_state is None:
            break
        state = prev_state

    # Remove one-window jitter.
    for i in range(1, len(shifts) - 1):
        if shifts[i - 1] == shifts[i + 1] and shifts[i] != shifts[i - 1]:
            shifts[i] = shifts[i - 1]

    changes = sum(1 for i in range(1, len(shifts)) if shifts[i] != shifts[i - 1])
    return shifts, window_ticks, changes


def summarize_windows(shifts: List[int]) -> str:
    if not shifts:
        return "w00-w00:+0"
    parts = []
    start = 0
    current = shifts[0]
    for i in range(1, len(shifts)):
        if shifts[i] != current:
            parts.append((start, i - 1, current))
            start = i
            current = shifts[i]
    parts.append((start, len(shifts) - 1, current))
    return ", ".join(f"w{s:02d}-w{e:02d}:{v:+d}" for s, e, v in parts)


def map_notes(
    notes: List[dict], shifts: List[int], window_ticks: int, tick_per_step: float
) -> Tuple[List[dict], float]:
    mapped = []
    total_dist = 0.0
    for n in notes:
        win = min(len(shifts) - 1, max(0, n["start"] // window_ticks))
        shift = shifts[win]
        pitch, dist = fold_and_snap(n["note"] + shift)
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


def assign_voices(
    mapped_notes: List[dict], melody_track: int, bass_track: int
) -> Tuple[Dict[str, List[Tuple[int, int, int]]], int]:
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)

    voices = {"A": [], "B": [], "C": []}
    short_removed = 0

    for step in sorted(by_start):
        src = by_start[step]
        filtered = []
        for n in src:
            is_short = n["dur_steps"] <= 1
            weak = (step % 2) == 1
            if is_short and weak and n["vel"] < 72 and n["track"] != melody_track:
                short_removed += 1
                continue
            filtered.append(n)
        if not filtered:
            continue

        filtered.sort(key=lambda x: (x["pitch"], x["track"]))
        strong = (step % 4) == 0
        eighth = (step % 2) == 0
        dense = len(filtered) >= 5
        used = set()

        # Voice A: always keep top note (melody-first).
        a_idx = len(filtered) - 1
        a_note = filtered[a_idx]
        voices["A"].append((step, a_note["end_step"], a_note["pitch"]))
        used.add(a_idx)

        if strong and len(filtered) >= 3:
            for i in range(len(filtered) - 2, -1, -1):
                if i in used:
                    continue
                iv = filtered[a_idx]["pitch"] - filtered[i]["pitch"]
                if 3 <= iv <= 10:
                    n = filtered[i]
                    voices["A"].append((step, n["end_step"], n["pitch"]))
                    used.add(i)
                    break

        # Voice C: bass anchor, reduced off-beat density when dense.
        bass_candidates = [
            i
            for i, n in enumerate(filtered)
            if i not in used and (n["track"] == bass_track or n["pitch"] <= 60)
        ]
        if not bass_candidates:
            bass_candidates = [i for i in range(len(filtered)) if i not in used]
        if bass_candidates and (not dense or strong or eighth):
            i = bass_candidates[0]
            n = filtered[i]
            voices["C"].append((step, n["end_step"], n["pitch"]))
            used.add(i)

        # Voice B: middle harmony with anti-mud.
        remaining = [(i, n) for i, n in enumerate(filtered) if i not in used]
        if remaining:
            if dense and not (strong or eighth):
                remaining = []
            keep = 1
            if strong and len(remaining) >= 2 and not dense:
                keep = 2
            mid = max(0, (len(remaining) - keep) // 2)
            for i in range(mid, min(len(remaining), mid + keep)):
                _, n = remaining[i]
                voices["B"].append((step, n["end_step"], n["pitch"]))

    return voices, short_removed


def merge_intervals(intervals: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
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
            if s <= cur_e + 1:
                cur_e = max(cur_e, e)
            else:
                merged.append((cur_s, cur_e, pitch))
                cur_s, cur_e = s, e
        merged.append((cur_s, cur_e, pitch))
    merged.sort(key=lambda x: (x[0], x[2], x[1]))
    return merged


def intervals_to_segments(
    intervals: List[Tuple[int, int, int]], total_steps: int, voice_name: str
) -> List[Tuple[int, int, Tuple[int, ...]]]:
    starts = defaultdict(list)
    ends = defaultdict(list)
    for s, e, p in intervals:
        s = max(0, s)
        e = min(total_steps, e)
        if e <= s:
            continue
        starts[s].append(p)
        ends[e].append(p)

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
        if voice_name == "A" and len(pitches) > 2:
            pitches = pitches[-2:]
        elif voice_name == "B" and len(pitches) > 2:
            m = len(pitches) // 2
            if len(pitches) % 2 == 0:
                pitches = pitches[m - 1 : m + 1]
            else:
                pitches = pitches[m - 1 : m + 1] if m > 0 else pitches[:2]
        elif voice_name == "C" and len(pitches) > 2:
            pitches = pitches[:2]

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


def pitch_to_domiso(pitch: int) -> str:
    pc = pitch % 12
    degree = DEGREE_BY_PC.get(pc)
    if degree is None:
        raise RuntimeError(f"Non-white mapped pitch encountered: {pitch}")
    octave = (pitch // 12) - 1  # MIDI standard
    shift = octave - 4
    prefix = ("+" * shift) if shift > 0 else ("-" * (-shift))
    return f"{prefix}{degree}"


def build_tempo_steps(tempo_nodes: List[Tuple[int, int]], tick_per_step: float) -> List[Tuple[int, int]]:
    tempo_steps = []
    for tick, bpm in tempo_nodes:
        step = int(round(tick / tick_per_step))
        if tempo_steps and tempo_steps[-1][0] == step:
            tempo_steps[-1] = (step, bpm)
        elif not tempo_steps or tempo_steps[-1][1] != bpm:
            tempo_steps.append((step, bpm))
    if not tempo_steps or tempo_steps[0][0] != 0:
        bpm0 = tempo_nodes[0][1] if tempo_nodes else 120
        tempo_steps.insert(0, (0, bpm0))
    return tempo_steps


def render_token(pitches: Tuple[int, ...], suffix: str) -> str:
    if not pitches:
        return "0" + suffix
    if len(pitches) == 1:
        return pitch_to_domiso(pitches[0]) + suffix
    body = " ".join(pitch_to_domiso(p) for p in sorted(pitches))
    return f"( {body} ){suffix}"


def serialize_voice(
    segments: List[Tuple[int, int, Tuple[int, ...]]], tempo_steps: List[Tuple[int, int]]
) -> List[str]:
    lines: List[str] = []
    current_line: List[str] = []
    tempo_idx = 0

    def flush_line():
        nonlocal current_line
        if current_line:
            lines.append(" ".join(current_line))
            current_line = []

    for seg_start, seg_end, pitches in segments:
        pos = seg_start
        while pos < seg_end:
            while tempo_idx < len(tempo_steps) and tempo_steps[tempo_idx][0] == pos:
                flush_line()
                lines.append(f"bpm={tempo_steps[tempo_idx][1]}")
                tempo_idx += 1

            while tempo_idx < len(tempo_steps) and tempo_steps[tempo_idx][0] < pos:
                tempo_idx += 1

            limit = seg_end - pos
            if tempo_idx < len(tempo_steps):
                step_to_tempo = tempo_steps[tempo_idx][0] - pos
                if step_to_tempo > 0:
                    limit = min(limit, step_to_tempo)

            chosen_len, suffix = 1, "//"
            for chunk_len, suf in CHUNK_SUFFIX:
                if chunk_len <= limit:
                    chosen_len, suffix = chunk_len, suf
                    break

            tok = render_token(pitches, suffix)
            current_line.append(tok)
            if len(" ".join(current_line)) > 120:
                last = current_line.pop()
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [last]

            pos += chosen_len

    flush_line()
    return lines


def tick_to_seconds(tick: int, tempo_nodes: List[Tuple[int, int]], tpb: int) -> float:
    if not tempo_nodes:
        return (tick / tpb) * 0.5
    nodes = sorted(tempo_nodes)
    if nodes[0][0] != 0:
        nodes.insert(0, (0, nodes[0][1]))
    sec = 0.0
    cur_tick = nodes[0][0]
    cur_bpm = nodes[0][1]
    for nxt_tick, nxt_bpm in nodes[1:]:
        if nxt_tick >= tick:
            break
        if nxt_tick > cur_tick:
            sec += (nxt_tick - cur_tick) / tpb * (60.0 / cur_bpm)
        cur_tick = nxt_tick
        cur_bpm = nxt_bpm
    if tick > cur_tick:
        sec += (tick - cur_tick) / tpb * (60.0 / cur_bpm)
    return sec


def normalize_output_base(name: str, max_len: int = 96) -> str:
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "-", name).strip().strip(".")
    safe = re.sub(r"\s+", "-", safe)
    safe = re.sub(r"-{2,}", "-", safe)
    if not safe:
        safe = "midi"
    if len(safe) > max_len:
        digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10]
        keep = max(1, max_len - len(digest) - 1)
        safe = f"{safe[:keep].rstrip('-_.')}-{digest}"
    return safe


def next_output_path(out_dir: str, midi_basename: str) -> str:
    safe_base = normalize_output_base(midi_basename)
    song_dir = os.path.join(out_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_domiso_arranged_v(\d+)_dense3layer\.txt$",
        re.IGNORECASE,
    )
    max_v = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            max_v = max(max_v, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_domiso_arranged_v{max_v + 1}_dense3layer.txt")


def lint_domiso_text(text: str):
    issues = []
    # Disallow accidental tokens like 1# / 2b after mapping.
    if re.search(r"(?<![A-Za-z0-9_])[+\-]*[1-7][#b](?![A-Za-z0-9_])", text):
        issues.append("Found accidental note tokens (#/b), expected white-key-only mapping.")
    if text.count("rollback=9999") != 2:
        issues.append("Expected exactly 2 rollback=9999 commands.")
    for voice in ("; Voice A", "; Voice B", "; Voice C"):
        if voice not in text:
            issues.append(f"Missing section marker: {voice}")
    return issues


def run(input_midi: str, out_dir: str):
    parsed = parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    max_tick = parsed["max_tick"]
    melody_track = parsed["melody_track"]
    bass_track = parsed["bass_track"]

    tempo_nodes = clean_tempos(parsed["tempos"], tpb)
    initial_bpm = tempo_nodes[0][1] if tempo_nodes else 120

    top_ids = build_top_ids(notes)
    base_shift = choose_base_shift(notes, top_ids, melody_track, tpb)
    shifts, window_ticks, change_count = choose_dynamic_shifts(
        notes, top_ids, melody_track, tpb, base_shift
    )

    tick_per_step = tpb / 4.0
    mapped_notes, total_dist = map_notes(notes, shifts, window_ticks, tick_per_step)
    voices, short_removed = assign_voices(mapped_notes, melody_track, bass_track)

    merged = {k: merge_intervals(v) for k, v in voices.items()}
    total_steps = max(n["end_step"] for n in mapped_notes) + 1

    tempo_steps = build_tempo_steps(tempo_nodes, tick_per_step)
    seg_a = intervals_to_segments(merged["A"], total_steps, "A")
    seg_b = intervals_to_segments(merged["B"], total_steps, "B")
    seg_c = intervals_to_segments(merged["C"], total_steps, "C")

    lines_a = serialize_voice(seg_a, tempo_steps)
    lines_b = serialize_voice(seg_b, tempo_steps)
    lines_c = serialize_voice(seg_c, tempo_steps)

    basename = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = next_output_path(out_dir, basename)
    title = basename.replace("-", " ").replace("_", " ").strip().title()
    duration_s = tick_to_seconds(max_tick, tempo_nodes, tpb)
    transpose_summary = summarize_windows(shifts)

    out_lines = [
        f"Title: {title} (arranged high-restore low-ornament)",
        f"Source: {os.path.basename(input_midi)}",
        f"Info: tempo {initial_bpm}, duration~{duration_s:.1f}s, grid 1/16",
        "Info: 3-layer restore, reduced weak short ornaments, source-derived only",
        f"Info: dynamic transpose windows(4 bars): {transpose_summary}",
        "",
        f"bpm={initial_bpm}",
        "",
        "; Voice A Melody (clean low-ornament)",
    ]
    out_lines.extend(lines_a)
    out_lines.extend(["", "rollback=9999", "", "; Voice B Harmony"])
    out_lines.extend(lines_b)
    out_lines.extend(["", "rollback=9999", "", "; Voice C Bass"])
    out_lines.extend(lines_c)
    out_text = "\n".join(out_lines).rstrip() + "\n"

    issues = lint_domiso_text(out_text)
    if issues:
        raise RuntimeError(" | ".join(issues))

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out_text)

    print(f"output={out_path}")
    print(f"notes={len(notes)}")
    print(f"tempo_raw={len(parsed['tempos'])} tempo_clean={len(tempo_nodes)}")
    print(f"base_transpose={base_shift} dynamic_changes={change_count}")
    print(f"window_summary={transpose_summary}")
    print(
        "voice_events="
        f"A:{len(merged['A'])} B:{len(merged['B'])} C:{len(merged['C'])}"
    )
    print(f"short_orn_removed={short_removed}")
    print(f"distortion_total={total_dist:.2f}")


def main():
    ap = argparse.ArgumentParser(
        description="Convert MIDI to DoMiSo 3-layer arrangement with low ornaments."
    )
    ap.add_argument("input_midi", help="Input MIDI file path")
    ap.add_argument(
        "--out-dir",
        default=r"d:\domiso\txt",
        help="Output directory (default: d:\\domiso\\txt)",
    )
    args = ap.parse_args()
    run(args.input_midi, args.out_dir)


if __name__ == "__main__":
    main()
