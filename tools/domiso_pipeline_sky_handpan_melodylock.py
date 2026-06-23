#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import domiso_pipeline_literal as base
import midi_to_domiso_dense3layer as core

HANDPAN_LAYOUT = "Y U I O / P H J K"
HANDPAN_NOTE_LABELS = ("D3", "A3", "C4", "D4", "F4", "G4", "A4", "C5")
HANDPAN_NOTE_INFO = "D3 A3 C4 D4 / F4 G4 A4 C5"
HANDPAN_SOUND_NOTES = (50, 57, 60, 62, 65, 67, 69, 72)
# Keep output pitches compatible with the existing Domiso Sky Handpan key map.
HANDPAN_NOTES = (60, 62, 64, 65, 67, 69, 71, 72)
HANDPAN_MIN = min(HANDPAN_NOTES)
HANDPAN_MAX = max(HANDPAN_NOTES)
HANDPAN_SOUND_MIN = min(HANDPAN_SOUND_NOTES)
HANDPAN_SOUND_MAX = max(HANDPAN_SOUND_NOTES)
HANDPAN_LEAD_FOCUS_MIN = 60
HANDPAN_LEAD_FOCUS_MAX = 72
HANDPAN_CENTER = 67
NOTE_NAMES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
SCALE_MODES = {
    "major": (0, 2, 4, 5, 7, 9, 11, 12),
    "minor": (0, 2, 3, 5, 7, 8, 10, 12),
    "dorian": (0, 2, 3, 5, 7, 9, 10, 12),
    "harmonic_minor": (0, 2, 3, 5, 7, 8, 11, 12),
}


@dataclass(frozen=True)
class StylePreset:
    min_gap_ms: int
    same_key_merge_ms: int
    min_duration_ms: int
    max_legato_ms: int


STYLE_PRESETS = {
    "faithful": StylePreset(
        min_gap_ms=70,
        same_key_merge_ms=110,
        min_duration_ms=100,
        max_legato_ms=520,
    ),
    "balanced": StylePreset(
        min_gap_ms=105,
        same_key_merge_ms=170,
        min_duration_ms=135,
        max_legato_ms=760,
    ),
    "smooth": StylePreset(
        min_gap_ms=145,
        same_key_merge_ms=240,
        min_duration_ms=190,
        max_legato_ms=1050,
    ),
}

ENSEMBLE_MAX_POLY = {
    "off": 1,
    "original": 2,
    "light": 2,
    "full": 3,
}
SOURCE_LITERAL_MAX_POLY = len(HANDPAN_NOTES)
SHORT_ADAPTED_MAX_POLY = 2


def latest_downloads_midi() -> Path:
    downloads = Path.home() / "Downloads"
    candidates = [
        p
        for p in downloads.iterdir()
        if p.is_file() and p.suffix.lower() in {".mid", ".midi"}
    ]
    if not candidates:
        raise FileNotFoundError(f"no .mid/.midi files found in {downloads}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def fold_and_snap_handpan(pitch: int) -> tuple[int, float]:
    folded = pitch
    while folded < HANDPAN_SOUND_MIN:
        folded += 12
    while folded > HANDPAN_SOUND_MAX:
        folded -= 12
    best_idx, best_sound = min(
        enumerate(HANDPAN_SOUND_NOTES),
        key=lambda item: (abs(item[1] - folded), abs(item[1] - pitch), abs(item[1] - HANDPAN_CENTER), item[0]),
    )
    return HANDPAN_NOTES[best_idx], float(abs(best_sound - folded))


def handpan_sound_pitch(key_pitch: int) -> int:
    return HANDPAN_SOUND_NOTES[HANDPAN_NOTES.index(key_pitch)]


def melodic_distance(a: int, b: int) -> int:
    return min(abs((a + octave) - b) for octave in (-12, 0, 12))


def pc_distance(a: int, b: int) -> int:
    diff = abs((a - b) % 12)
    return min(diff, 12 - diff)


def direction_sign(value: int) -> int:
    return (value > 0) - (value < 0)


def weighted_percentile(items: list[tuple[int, float]], percentile: float) -> float:
    if not items:
        return 60.0
    ordered = sorted(items, key=lambda item: item[0])
    total = sum(max(0.0, weight) for _, weight in ordered)
    if total <= 0:
        mid = len(ordered) // 2
        return float(ordered[mid][0])
    target = total * percentile
    seen = 0.0
    for value, weight in ordered:
        seen += max(0.0, weight)
        if seen >= target:
            return float(value)
    return float(ordered[-1][0])


def note_weight(note: dict, idx: int, top_ids: set[int], tpb: int) -> float:
    duration = max(1, int(note["end"]) - int(note["start"]))
    weight = 1.0 + min(2.4, duration / max(1.0, tpb / 2.0))
    weight += int(note["vel"]) / 110.0
    if idx in top_ids:
        weight += 1.4
    if round(int(note["start"]) / max(1, tpb / 4.0)) % 4 == 0:
        weight += 0.45
    return weight


def track_lead_scores(notes: list[dict], top_ids: set[int]) -> dict[int, float]:
    by_track: dict[int, list[tuple[int, dict]]] = defaultdict(list)
    for idx, note in enumerate(notes):
        by_track[int(note["track"])].append((idx, note))
    scores: dict[int, float] = {}
    for track, entries in by_track.items():
        pitches = [int(n["note"]) for _, n in entries]
        starts = [int(n["start"]) for _, n in entries]
        unique_starts = len(set(starts))
        note_count = len(entries)
        if not note_count:
            continue
        median_pitch = statistics.median(pitches)
        top_ratio = sum(1 for idx, _ in entries if idx in top_ids) / note_count
        mono_ratio = unique_starts / note_count
        density = min(1.0, unique_starts / max(1, len({int(n["start"]) for n in notes})))
        score = 0.0
        score += top_ratio * 5.0
        score += mono_ratio * 2.2
        score += density * 1.2
        score += min(1.5, max(0.0, (median_pitch - 54) / 18.0))
        if note_count < 12:
            score -= 2.0
        scores[track] = score
    return scores


def raw_lead_score(
    note: dict,
    idx: int,
    *,
    top_ids: set[int],
    track_scores: dict[int, float],
    prev_note: dict | None,
    step: int,
) -> float:
    pitch = int(note["note"])
    track = int(note["track"])
    score = track_scores.get(track, 0.0)
    if idx in top_ids:
        score += 3.8
    if step % 16 == 0:
        score += 1.5
    elif step % 4 == 0:
        score += 0.7
    duration = int(note["end"]) - int(note["start"])
    score += min(1.4, duration / 240.0)
    score += int(note["vel"]) / 150.0
    score += min(1.2, max(0.0, (pitch - 58) / 18.0))
    if prev_note is not None:
        prev_pitch = int(prev_note["note"])
        dist = melodic_distance(pitch, prev_pitch)
        if dist <= 2:
            score += 1.2
        elif dist <= 5:
            score += 0.8
        elif dist <= 9:
            score += 0.2
        elif dist >= 14:
            score -= 1.2
    return score


def select_raw_lead_notes(
    notes: list[dict],
    top_ids: set[int],
    tpb: int,
    *,
    preferred_track: int | None = None,
    blend_tracks: bool = False,
) -> tuple[set[int], dict[str, object]]:
    track_scores = track_lead_scores(notes, top_ids)
    best_track_score = max(track_scores.values()) if track_scores else 0.0
    if preferred_track is not None:
        lead_tracks = {preferred_track}
    elif blend_tracks:
        lead_tracks = {track for track, score in track_scores.items() if score >= best_track_score - 1.75}
    elif track_scores:
        lead_tracks = {max(track_scores, key=track_scores.get)}
    else:
        lead_tracks = set()
    by_start: dict[int, list[tuple[int, dict]]] = defaultdict(list)
    for idx, note in enumerate(notes):
        by_start[int(note["start"])].append((idx, note))

    selected_ids: set[int] = set()
    selected_tracks: Counter[int] = Counter()
    prev_note: dict | None = None
    rejected_low_score = 0
    rejected_nonlead_track = 0
    for step in sorted(by_start):
        raw_candidates = by_start[step]
        candidates = [
            (idx, note)
            for idx, note in raw_candidates
            if int(note["track"]) in lead_tracks
            or (
                blend_tracks
                and idx in top_ids
                and track_scores.get(int(note["track"]), 0.0) >= best_track_score - 2.35
                and int(note["note"]) >= 60
            )
        ]
        if not candidates:
            rejected_nonlead_track += 1
            continue
        scored = [
            (
                raw_lead_score(
                    note,
                    idx,
                    top_ids=top_ids,
                    track_scores=track_scores,
                    prev_note=prev_note,
                    step=round(step / max(1, tpb / 4.0)),
                ),
                idx,
                note,
            )
            for idx, note in candidates
        ]
        scored.sort(key=lambda item: (item[0], int(item[2]["note"]), int(item[2]["vel"])), reverse=True)
        score, idx, note = scored[0]
        strong = (round(step / max(1, tpb / 4.0)) % 4) == 0
        if score < 3.2 and not strong:
            rejected_low_score += 1
            continue
        selected_ids.add(idx)
        selected_tracks[int(note["track"])] += 1
        prev_note = note

    if preferred_track is not None:
        primary_track = preferred_track
    elif selected_tracks:
        primary_track = selected_tracks.most_common(1)[0][0]
    else:
        primary_track = int(max(track_scores, key=track_scores.get))
    return selected_ids, {
        "raw_lead_candidates": len(selected_ids),
        "primary_lead_track": primary_track,
        "allowed_lead_tracks": sorted(lead_tracks),
        "blend_lead_tracks": blend_tracks,
        "lead_track_scores": {str(k): round(v, 3) for k, v in sorted(track_scores.items())},
        "lead_tracks_used": dict(sorted(selected_tracks.items())),
        "lead_rejected_low_score": rejected_low_score,
        "lead_rejected_nonlead_track": rejected_nonlead_track,
    }


def detect_scale(
    notes: list[dict],
    lead_ids: set[int],
    top_ids: set[int],
    tpb: int,
) -> dict[str, object]:
    weighted_notes = [
        (int(note["note"]), note_weight(note, idx, top_ids, tpb))
        for idx, note in enumerate(notes)
        if idx in lead_ids
    ]
    if not weighted_notes:
        weighted_notes = [(int(note["note"]), note_weight(note, idx, top_ids, tpb)) for idx, note in enumerate(notes)]

    best = None
    for tonic in range(12):
        for mode, intervals in SCALE_MODES.items():
            scale_pcs = {(tonic + interval) % 12 for interval in intervals[:-1]}
            score = 0.0
            for pitch, weight in weighted_notes:
                pc = pitch % 12
                dist = min(pc_distance(pc, scale_pc) for scale_pc in scale_pcs)
                score -= dist * weight
                if pc == tonic:
                    score += 0.42 * weight
                if pc == (tonic + 7) % 12:
                    score += 0.18 * weight
                if pc in scale_pcs:
                    score += 0.22 * weight
            if best is None or score > best["score"]:
                best = {
                    "tonic_pc": tonic,
                    "tonic": NOTE_NAMES[tonic],
                    "mode": mode,
                    "score": round(score, 3),
                    "intervals": intervals,
                }
    assert best is not None
    return best


def build_contour_mapping(
    notes: list[dict],
    lead_ids: set[int],
    top_ids: set[int],
    tpb: int,
) -> dict[str, object]:
    weighted = [
        (int(note["note"]), note_weight(note, idx, top_ids, tpb))
        for idx, note in enumerate(notes)
        if idx in lead_ids
    ]
    if not weighted:
        weighted = [(int(note["note"]), note_weight(note, idx, top_ids, tpb)) for idx, note in enumerate(notes)]
    low = int(round(weighted_percentile(weighted, 0.08)))
    high = int(round(weighted_percentile(weighted, 0.92)))
    if high - low < 7:
        center = int(round(weighted_percentile(weighted, 0.50)))
        low = center - 4
        high = center + 4
    return {
        "low": low,
        "high": high,
        "span": max(1, high - low),
    }


def map_pitch_contour(pitch: int, contour: dict[str, object]) -> tuple[int, float, int]:
    low = int(contour["low"])
    span = max(1, int(contour["span"]))
    ratio = (pitch - low) / span
    idx = int(round(max(0.0, min(1.0, ratio)) * (len(HANDPAN_NOTES) - 1)))
    mapped = HANDPAN_NOTES[idx]
    ideal = low + (idx / (len(HANDPAN_NOTES) - 1)) * span
    return mapped, abs(pitch - ideal), idx


def map_pitch_scale(pitch: int, scale: dict[str, object]) -> tuple[int, float, int]:
    tonic = int(scale["tonic_pc"])
    intervals = tuple(int(x) for x in scale["intervals"])
    best = None
    for octave in range(-2, 9):
        base_pitch = tonic + 12 * octave
        for idx, interval in enumerate(intervals):
            candidate = base_pitch + interval
            dist = abs(candidate - pitch)
            if best is None or (dist, abs(idx - 3.5), idx) < best[0]:
                best = ((dist, abs(idx - 3.5), idx), idx, candidate)
    assert best is not None
    idx = best[1]
    return HANDPAN_NOTES[idx], float(best[0][0]), idx


def target_handpan_tonic(scale: dict[str, object]) -> int:
    mode = str(scale["mode"])
    if mode == "major":
        return 5  # F major pentatonic on Sky handpan in C-key environments.
    if mode in {"minor", "harmonic_minor", "dorian"}:
        return 2  # D minor pentatonic / D dorian subset.
    return 5


def key_shift_candidates(scale: dict[str, object]) -> list[int]:
    tonic = int(scale["tonic_pc"])
    target = target_handpan_tonic(scale)
    base = (target - tonic) % 12
    candidates = {base + 12 * octave for octave in range(-2, 3)}
    return sorted(shift for shift in candidates if -12 <= shift <= 12)


def choose_key_shift(notes: list[dict], top_ids: set[int], lead_ids: set[int], tpb: int, scale: dict[str, object]) -> int:
    entries = list(enumerate(notes))
    candidates = key_shift_candidates(scale)
    if not candidates:
        return 0
    return min(
        candidates,
        key=lambda shift: (
            evaluate_shift_cost_entries(entries, shift, lead_ids, top_ids, tpb)
            + shift_contour_cost_entries(entries, shift, lead_ids) * 500.0
            + abs(shift) * 0.6,
            shift,
        ),
    )


def shift_contour_cost_entries(entries: list[tuple[int, dict]], shift: int, lead_ids: set[int]) -> float:
    lead_entries = [
        (int(note["start"]), int(note["note"]))
        for idx, note in entries
        if idx in lead_ids
    ]
    lead_entries.sort()
    if len(lead_entries) < 2:
        return 0.0

    penalty = 0.0
    compared = 0
    prev_start, prev_src = lead_entries[0]
    prev_mapped = handpan_sound_pitch(fold_and_snap_handpan(prev_src + shift)[0])
    for start, src in lead_entries[1:]:
        if start == prev_start:
            continue
        mapped = handpan_sound_pitch(fold_and_snap_handpan(src + shift)[0])
        src_delta = src - prev_src
        mapped_delta = mapped - prev_mapped
        if src_delta != 0:
            compared += 1
            if mapped_delta == 0:
                penalty += 1.8
            elif direction_sign(src_delta) != direction_sign(mapped_delta):
                penalty += 3.8
            if abs(src_delta) <= 2 and abs(mapped_delta) >= 7:
                penalty += 1.4
            penalty += min(1.0, abs(abs(mapped_delta) - abs(src_delta)) * 0.08)
        prev_start = start
        prev_src = src
        prev_mapped = mapped
    return penalty / max(1, compared)


def evaluate_shift_cost_entries(
    entries: list[tuple[int, dict]],
    shift: int,
    lead_ids: set[int],
    top_ids: set[int],
    tpb: int,
) -> float:
    total = 0.0
    short_limit = max(1, tpb // 6)
    for idx, note in entries:
        mapped, dist = fold_and_snap_handpan(int(note["note"]) + shift)
        weight = 1.0
        if idx in lead_ids:
            weight += 5.2
        elif idx in top_ids:
            weight += 1.4
        if int(note["end"]) - int(note["start"]) <= short_limit:
            weight *= 0.72
        total += dist * weight
        if idx in lead_ids:
            mapped_sound = handpan_sound_pitch(mapped)
            if mapped_sound < HANDPAN_LEAD_FOCUS_MIN:
                total += (HANDPAN_LEAD_FOCUS_MIN - mapped_sound) * 0.14
            elif mapped_sound > HANDPAN_LEAD_FOCUS_MAX:
                total += (mapped_sound - HANDPAN_LEAD_FOCUS_MAX) * 0.10
    return total


def choose_base_shift(notes: list[dict], top_ids: set[int], lead_ids: set[int], tpb: int) -> int:
    entries = list(enumerate(notes))
    best_shift = 0
    best_cost = float("inf")
    for shift in range(-12, 13):
        cost = evaluate_shift_cost_entries(entries, shift, lead_ids, top_ids, tpb) + abs(shift) * 0.16
        if cost < best_cost:
            best_shift = shift
            best_cost = cost
    return best_shift


def choose_dynamic_shifts(
    notes: list[dict],
    top_ids: set[int],
    lead_ids: set[int],
    tpb: int,
    base_shift: int,
) -> tuple[list[int], int, int]:
    window_ticks = max(1, tpb * 16)
    max_window = max(int(n["start"]) // window_ticks for n in notes)
    count = max_window + 1
    candidates = sorted({base_shift + d for d in (0, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5) if -12 <= base_shift + d <= 12})
    by_window: dict[int, list[tuple[int, dict]]] = defaultdict(list)
    for idx, note in enumerate(notes):
        by_window[int(note["start"]) // window_ticks].append((idx, note))

    local_costs: list[dict[int, float]] = []
    for window in range(count):
        entries = by_window.get(window, [])
        costs = {}
        for shift in candidates:
            costs[shift] = evaluate_shift_cost_entries(entries, shift, lead_ids, top_ids, tpb)
        local_costs.append(costs)

    max_changes = 4
    dp = {(shift, 0): local_costs[0][shift] for shift in candidates}
    back: list[dict[tuple[int, int], tuple[int, int] | None]] = [{(shift, 0): None for shift in candidates}]
    for window in range(1, count):
        next_dp = {}
        next_back = {}
        for shift in candidates:
            for (prev_shift, changes), prev_cost in dp.items():
                next_changes = changes + (1 if shift != prev_shift else 0)
                if next_changes > max_changes:
                    continue
                cost = prev_cost + local_costs[window][shift]
                if shift != prev_shift:
                    cost += 3.0 + 0.3 * abs(shift - prev_shift)
                key = (shift, next_changes)
                if key not in next_dp or cost < next_dp[key]:
                    next_dp[key] = cost
                    next_back[key] = (prev_shift, changes)
        if not next_dp:
            next_dp = {(base_shift, 0): min(dp.values())}
            next_back = {(base_shift, 0): min(dp, key=lambda k: dp[k])}
        dp = next_dp
        back.append(next_back)

    state = min(dp, key=lambda k: dp[k])
    shifts = [base_shift] * count
    for window in range(count - 1, -1, -1):
        shifts[window] = state[0]
        prev = back[window].get(state)
        if prev is None:
            break
        state = prev
    changes = sum(1 for i in range(1, len(shifts)) if shifts[i] != shifts[i - 1])
    return shifts, window_ticks, changes


def build_tempo_steps(tempos: list[tuple[int, float]], tick_per_step: float) -> list[tuple[int, int]]:
    return core.build_tempo_steps([(tick, int(round(bpm))) for tick, bpm in tempos], tick_per_step)


def build_step_ms(total_steps: int, tempo_steps: list[tuple[int, int]]) -> list[float]:
    ms = [0.0] * (total_steps + 1)
    if total_steps <= 0:
        return ms
    tempo_idx = 0
    bpm = tempo_steps[0][1] if tempo_steps else 120
    for step in range(total_steps):
        while tempo_idx + 1 < len(tempo_steps) and tempo_steps[tempo_idx + 1][0] <= step:
            tempo_idx += 1
            bpm = tempo_steps[tempo_idx][1]
        ms[step + 1] = ms[step] + (60000.0 / bpm / 4.0)
    return ms


def map_notes(
    parsed: dict,
    mapping_mode: str,
    *,
    preferred_lead_track: int | None = None,
    blend_lead_tracks: bool = False,
) -> tuple[list[dict], dict[str, object]]:
    notes = parsed["notes"]
    tpb = parsed["tpb"]
    top_ids = core.build_top_ids(notes)
    raw_lead_ids, lead_stats = select_raw_lead_notes(
        notes,
        top_ids,
        tpb,
        preferred_track=preferred_lead_track,
        blend_tracks=blend_lead_tracks,
    )
    melody_track = int(lead_stats["primary_lead_track"])
    key_info = detect_scale(notes, raw_lead_ids, top_ids, tpb)
    contour_info = build_contour_mapping(notes, raw_lead_ids, top_ids, tpb)
    if mapping_mode == "snap":
        base_shift = choose_base_shift(notes, top_ids, raw_lead_ids, tpb)
        shifts, window_ticks, shift_changes = choose_dynamic_shifts(notes, top_ids, raw_lead_ids, tpb, base_shift)
    elif mapping_mode == "keyshift":
        window_ticks = max(1, tpb * 16)
        max_window = max(int(n["start"]) // window_ticks for n in notes)
        base_shift = choose_key_shift(notes, top_ids, raw_lead_ids, tpb, key_info)
        shifts = [base_shift] * (max_window + 1)
        shift_changes = 0
    else:
        window_ticks = max(1, tpb * 16)
        max_window = max(int(n["start"]) // window_ticks for n in notes)
        shifts = [0] * (max_window + 1)
        base_shift = 0
        shift_changes = 0
    tick_per_step = tpb / 4.0
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    mapped = []
    mapping_indices: Counter[int] = Counter()
    total_dist = 0.0
    for idx, note in enumerate(notes):
        window = min(len(shifts) - 1, max(0, int(note["start"]) // window_ticks))
        if mapping_mode == "literal":
            pitch, dist = fold_and_snap_handpan(int(note["note"]))
            map_index = HANDPAN_NOTES.index(pitch)
        elif mapping_mode == "contour":
            pitch, dist, map_index = map_pitch_contour(int(note["note"]), contour_info)
        elif mapping_mode == "scale":
            pitch, dist, map_index = map_pitch_scale(int(note["note"]), key_info)
        elif mapping_mode == "keyshift":
            pitch, dist = fold_and_snap_handpan(int(note["note"]) + shifts[window])
            map_index = HANDPAN_NOTES.index(pitch)
        else:
            pitch, dist = fold_and_snap_handpan(int(note["note"]) + shifts[window])
            map_index = HANDPAN_NOTES.index(pitch)
        sound_pitch = HANDPAN_SOUND_NOTES[map_index]
        if mapping_mode == "literal" or idx in raw_lead_ids or not raw_lead_ids:
            mapping_indices[map_index] += 1
            total_dist += dist
        start_step = int(round(int(note["start"]) / tick_per_step))
        end_step = int(round(int(note["end"]) / tick_per_step))
        if end_step <= start_step:
            end_step = start_step + 1
        mapped.append(
            {
                **note,
                "src_idx": idx,
                "src_note": int(note["note"]),
                "pitch": pitch,
                "sound_pitch": sound_pitch,
                "dist": dist,
                "map_index": map_index,
                "is_top": idx in top_ids,
                "is_raw_lead": idx in raw_lead_ids,
                "is_melody_track": int(note["track"]) == melody_track,
                "start_step": start_step,
                "end_step": end_step,
                "dur_steps": end_step - start_step,
            }
        )
    return mapped, {
        "top_ids": top_ids,
        "raw_lead_ids": raw_lead_ids,
        "lead_stats": lead_stats,
        "melody_track": melody_track,
        "mapping_mode": mapping_mode,
        "detected_key": f"{key_info['tonic']} {key_info['mode']}",
        "detected_key_score": key_info["score"],
        "key_shift_target": NOTE_NAMES[target_handpan_tonic(key_info)],
        "contour_low": contour_info["low"],
        "contour_high": contour_info["high"],
        "lead_mapping_index_counts": dict(sorted(mapping_indices.items())),
        "lead_mapping_total_dist": round(total_dist, 2),
        "base_shift": base_shift,
        "shifts": shifts,
        "window_ticks": window_ticks,
        "shift_changes": shift_changes,
        "shift_summary": core.summarize_windows(shifts),
        "tempos": tempos,
        "tempo_steps": build_tempo_steps(tempos, tick_per_step),
        "tick_per_step": tick_per_step,
    }


def score_lead(note: dict, prev_pitch: int | None, step: int) -> float:
    score = 0.0
    sound_pitch = int(note.get("sound_pitch", note["pitch"]))
    if note.get("is_raw_lead"):
        score += 7.0
    if note["is_melody_track"]:
        score += 2.0
    if note["is_top"]:
        score += 1.8
    if step % 16 == 0:
        score += 2.2
    elif step % 4 == 0:
        score += 1.0
    score += min(1.5, int(note["dur_steps"]) * 0.3)
    score += int(note["vel"]) / 120.0
    if HANDPAN_LEAD_FOCUS_MIN <= sound_pitch <= HANDPAN_LEAD_FOCUS_MAX:
        score += 0.5
    elif sound_pitch < HANDPAN_LEAD_FOCUS_MIN:
        score -= 0.35
    if prev_pitch is not None:
        leap = abs(sound_pitch - prev_pitch)
        if leap <= 2:
            score += 0.8
        elif leap <= 5:
            score += 0.4
        elif leap >= 9:
            score -= 0.8
    return score


def select_candidate(candidates: list[dict], prev_pitch: int | None, step: int) -> dict | None:
    raw_lead = [n for n in candidates if n.get("is_raw_lead")]
    if not raw_lead:
        return None
    return max(raw_lead, key=lambda n: score_lead(n, prev_pitch, step))


def build_melody_intervals(
    mapped: list[dict],
    melody_track: int,
    preset: StylePreset,
    step_ms: list[float],
) -> tuple[list[tuple[int, int, int]], dict[str, object]]:
    by_step: dict[int, list[dict]] = defaultdict(list)
    for note in mapped:
        by_step[int(note["start_step"])].append(note)

    raw = []
    prev_pitch = None
    melody_track_count = 0
    fallback_count = 0
    non_primary_track_count = 0
    raw_lead_count = 0
    top_count = 0
    source_tracks: Counter[int] = Counter()
    for step in sorted(by_step):
        candidate = select_candidate(by_step[step], prev_pitch, step)
        if candidate is None:
            continue
        raw.append(dict(candidate))
        prev_pitch = int(candidate.get("sound_pitch", candidate["pitch"]))
        source_tracks[int(candidate["track"])] += 1
        if candidate.get("is_raw_lead"):
            raw_lead_count += 1
        if candidate["is_top"]:
            top_count += 1
        if int(candidate["track"]) == melody_track:
            melody_track_count += 1
        else:
            non_primary_track_count += 1
        if not candidate.get("is_raw_lead"):
            fallback_count += 1

    def time_at(step: int) -> float:
        return step_ms[min(max(0, step), len(step_ms) - 1)] if step_ms else 0.0

    kept: list[dict] = []
    dropped_by_rate = 0
    merged_same_key = 0
    replaced = 0
    for idx, note in enumerate(raw):
        step = int(note["start_step"])
        pitch = int(note["pitch"])
        sound_pitch = int(note.get("sound_pitch", pitch))
        strong = step % 4 == 0
        prev_note = raw[idx - 1] if idx > 0 else None
        next_note = raw[idx + 1] if idx + 1 < len(raw) else None
        prev_pitch_raw = int(prev_note.get("sound_pitch", prev_note["pitch"])) if prev_note else None
        next_pitch_raw = int(next_note.get("sound_pitch", next_note["pitch"])) if next_note else None
        contour = (
            prev_pitch_raw is not None
            and next_pitch_raw is not None
            and (
                (sound_pitch > prev_pitch_raw and sound_pitch > next_pitch_raw)
                or (sound_pitch < prev_pitch_raw and sound_pitch < next_pitch_raw)
            )
        )
        if kept:
            prev = kept[-1]
            gap_ms = time_at(step) - time_at(int(prev["start_step"]))
            same_key = pitch == int(prev["pitch"])
            same_source_pitch = int(note["src_note"]) == int(prev["src_note"])
            if same_key and gap_ms <= preset.same_key_merge_ms and (same_source_pitch or (gap_ms < preset.min_gap_ms and not strong)):
                prev["end_step"] = max(int(prev["end_step"]), int(note["end_step"]))
                merged_same_key += 1
                continue
            if gap_ms < preset.min_gap_ms and not strong:
                if contour and not same_key and score_lead(note, int(prev["pitch"]), step) > score_lead(prev, None, int(prev["start_step"])) + 0.8:
                    kept[-1] = note
                    replaced += 1
                else:
                    dropped_by_rate += 1
                continue
        kept.append(note)

    intervals = []
    legato_extended = 0
    min_duration_extended = 0
    same_key_cuts = 0
    for idx, note in enumerate(kept):
        start = int(note["start_step"])
        end = max(start + 1, int(note["end_step"]))
        pitch = int(note["pitch"])
        if idx + 1 < len(kept):
            next_start = int(kept[idx + 1]["start_step"])
            next_pitch = int(kept[idx + 1]["pitch"])
            gap_ms = time_at(next_start) - time_at(start)
            if gap_ms <= preset.max_legato_ms:
                target = next_start if next_pitch != pitch else max(start + 1, next_start - 1)
                if next_pitch == pitch:
                    same_key_cuts += 1
                if target > end:
                    end = target
                    legato_extended += 1
                elif end > target:
                    end = target
        current_ms = time_at(end) - time_at(start)
        if current_ms < preset.min_duration_ms:
            one_step = max(1.0, time_at(start + 1) - time_at(start))
            proposed = start + max(1, int(math.ceil(preset.min_duration_ms / one_step)))
            if idx + 1 < len(kept):
                proposed = min(proposed, int(kept[idx + 1]["start_step"]))
            if proposed > end:
                end = proposed
                min_duration_extended += 1
        intervals.append((start, max(start + 1, end), pitch))

    return base.merge_intervals_strict(intervals), {
        "source_notes": len(mapped),
        "raw_lead_candidates": len(raw),
        "kept_lead_notes": len(kept),
        "melody_track": melody_track,
        "lead_from_raw_lead": raw_lead_count,
        "lead_from_melody_track": melody_track_count,
        "lead_from_non_primary_track": non_primary_track_count,
        "lead_from_top_note": top_count,
        "fallback_lead_notes": fallback_count,
        "source_tracks_used": dict(sorted(source_tracks.items())),
        "dropped_by_rate": dropped_by_rate,
        "merged_same_key": merged_same_key,
        "replaced_by_contour": replaced,
        "legato_extended": legato_extended,
        "min_duration_extended": min_duration_extended,
        "same_key_release_cuts": same_key_cuts,
        "output_intervals": len(intervals),
    }


def build_literal_source_intervals(mapped: list[dict]) -> tuple[list[tuple[int, int, int]], dict[str, object]]:
    intervals = [
        (int(note["start_step"]), max(int(note["start_step"]) + 1, int(note["end_step"])), int(note["pitch"]))
        for note in mapped
    ]
    merged = base.merge_intervals_strict(intervals)
    source_tracks: Counter[int] = Counter(int(note["track"]) for note in mapped)
    source_pitches = [int(note["src_note"]) for note in mapped]
    mapped_sounds = [int(note["sound_pitch"]) for note in mapped]
    return merged, {
        "source_notes": len(mapped),
        "literal_source_tracks_used": dict(sorted(source_tracks.items())),
        "literal_source_pitch_range": f"{min(source_pitches)}..{max(source_pitches)}" if source_pitches else "",
        "literal_handpan_sound_range": f"{min(mapped_sounds)}..{max(mapped_sounds)}" if mapped_sounds else "",
        "literal_merged_same_key_overlaps": len(intervals) - len(merged),
        "raw_lead_candidates": 0,
        "kept_lead_notes": 0,
        "melody_track": "all",
        "lead_from_raw_lead": 0,
        "lead_from_melody_track": 0,
        "lead_from_non_primary_track": 0,
        "lead_from_top_note": 0,
        "fallback_lead_notes": 0,
        "source_tracks_used": dict(sorted(source_tracks.items())),
        "dropped_by_rate": 0,
        "merged_same_key": len(intervals) - len(merged),
        "replaced_by_contour": 0,
        "legato_extended": 0,
        "min_duration_extended": 0,
        "same_key_release_cuts": 0,
        "output_intervals": len(merged),
    }


def build_short_tail_intervals(
    melody_intervals: list[tuple[int, int, int]],
    mapped: list[dict],
    total_steps: int,
) -> tuple[list[tuple[int, int, int]], dict[str, object]]:
    if not melody_intervals:
        return [], {
            "short_tail_lead_taps": 0,
            "short_tail_rehits": 0,
            "short_tail_support_notes": 0,
            "short_tail_total_intervals": 0,
        }

    ordered = sorted(melody_intervals, key=lambda item: (item[0], item[1], item[2]))
    lead_taps: list[tuple[int, int, int]] = []
    occupied_lead_starts: set[int] = set()
    rehit_count = 0

    def add_tap(target: list[tuple[int, int, int]], step: int, duration: int, pitch: int) -> bool:
        if step < 0 or step >= total_steps:
            return False
        end = min(total_steps, step + max(1, duration))
        if end <= step:
            return False
        target.append((step, end, pitch))
        return True

    for idx, (start, end, pitch) in enumerate(ordered):
        next_start = ordered[idx + 1][0] if idx + 1 < len(ordered) else total_steps
        stop = min(end, next_start)
        if stop <= start:
            stop = min(total_steps, start + 1)
        duration = 2 if stop - start >= 2 else 1
        if add_tap(lead_taps, start, duration, pitch):
            occupied_lead_starts.add(start)

        span = stop - start
        if span >= 10:
            first_rehit = start + 8
            step = first_rehit + ((4 - first_rehit % 4) % 4)
            local_rehits = 0
            while step < stop - 2 and step < next_start - 2 and local_rehits < 2:
                if step not in occupied_lead_starts:
                    if add_tap(lead_taps, step, 1, pitch):
                        occupied_lead_starts.add(step)
                        rehit_count += 1
                        local_rehits += 1
                step += 16

    active_lead_by_step: dict[int, set[int]] = defaultdict(set)
    for start, end, pitch in lead_taps:
        for step in range(start, min(end, total_steps)):
            active_lead_by_step[step].add(pitch)

    by_source_step: dict[int, list[dict]] = defaultdict(list)
    first_start = min(start for start, _, _ in ordered)
    last_end = max(end for _, end, _ in ordered)
    for note in mapped:
        if note.get("is_raw_lead"):
            continue
        step = int(note["start_step"])
        if step < first_start or step >= last_end:
            continue
        if step in occupied_lead_starts:
            continue
        if step % 8 != 0:
            continue
        by_source_step[step].append(note)

    support: list[tuple[int, int, int]] = []
    support_by_bar: Counter[int] = Counter()
    last_support = -999

    def support_score(note: dict, step: int) -> float:
        sound_pitch = int(note.get("sound_pitch", note["pitch"]))
        dur_steps = max(1, int(note["dur_steps"]))
        score = min(1.5, dur_steps / 8.0) + int(note.get("vel", 64)) / 180.0
        if not note.get("is_melody_track"):
            score += 1.0
        if step % 16 == 0:
            score += 1.0
        if sound_pitch <= 57:
            score += 0.8
        elif sound_pitch <= 62:
            score += 0.5
        elif sound_pitch >= 69:
            score -= 0.4
        score -= float(note.get("dist", 0.0)) * 0.05
        return score

    for step in sorted(by_source_step):
        bar = step // 16
        if support_by_bar[bar] >= 1 or step - last_support < 16:
            continue
        active = active_lead_by_step.get(step, set())
        candidates = [note for note in by_source_step[step] if int(note["pitch"]) not in active]
        if not candidates:
            continue
        chosen = max(candidates, key=lambda note: support_score(note, step))
        if add_tap(support, step, 1, int(chosen["pitch"])):
            support_by_bar[bar] += 1
            last_support = step

    combined = base.merge_intervals_strict(lead_taps + support)
    return combined, {
        "short_tail_lead_taps": len(lead_taps),
        "short_tail_rehits": rehit_count,
        "short_tail_support_notes": len(support),
        "short_tail_total_intervals": len(combined),
    }


def nearest_handpan_slot(pc: int, *, prefer_low: bool, avoid: set[int] | None = None) -> int:
    avoid = avoid or set()
    candidates = [
        (idx, pitch)
        for idx, pitch in enumerate(HANDPAN_SOUND_NOTES)
        if idx not in avoid
    ]
    if not candidates:
        candidates = list(enumerate(HANDPAN_SOUND_NOTES))
    center = 57 if prefer_low else 65
    return min(
        candidates,
        key=lambda item: (
            pc_distance(item[1] % 12, pc),
            abs(item[1] - center),
            item[0],
        ),
    )[0]


def support_slots(mapping: dict[str, object]) -> dict[str, int]:
    tonic_name = str(mapping.get("key_shift_target") or "D")
    tonic_pc = NOTE_NAMES.index(tonic_name) if tonic_name in NOTE_NAMES else 2
    minorish = tonic_pc == 2
    third_pc = (tonic_pc + (3 if minorish else 4)) % 12
    fifth_pc = (tonic_pc + 7) % 12

    tonic = nearest_handpan_slot(tonic_pc, prefer_low=True)
    fifth = nearest_handpan_slot(fifth_pc, prefer_low=True, avoid={tonic})
    third = nearest_handpan_slot(third_pc, prefer_low=False, avoid={tonic, fifth})
    color = nearest_handpan_slot((tonic_pc + 2) % 12, prefer_low=False, avoid={tonic, fifth, third})
    return {
        "tonic": HANDPAN_NOTES[tonic],
        "fifth": HANDPAN_NOTES[fifth],
        "third": HANDPAN_NOTES[third],
        "color": HANDPAN_NOTES[color],
    }


def active_pitches_at(intervals: list[tuple[int, int, int]], step: int) -> set[int]:
    return {pitch for start, end, pitch in intervals if start <= step < end}


def melody_start_counts(intervals: list[tuple[int, int, int]], start: int, end: int) -> int:
    return sum(1 for note_start, _, _ in intervals if start <= note_start < end)


def harmony_echo_pitch(melody_pitch: int, slots: dict[str, int]) -> int:
    idx = HANDPAN_NOTES.index(melody_pitch)
    if idx >= 6:
        return slots["third"]
    if idx >= 4:
        return slots["fifth"]
    if idx <= 1:
        return slots["color"]
    return slots["tonic"]


def build_ensemble_intervals(
    melody_intervals: list[tuple[int, int, int]],
    mapped: list[dict],
    total_steps: int,
    mapping: dict[str, object],
    ensemble_style: str,
) -> tuple[list[tuple[int, int, int]], dict[str, object]]:
    max_poly = ENSEMBLE_MAX_POLY[ensemble_style]
    if not melody_intervals:
        return melody_intervals, {
            "ensemble_enabled": True,
            "ensemble_style": ensemble_style,
            "ensemble_support_notes": 0,
            "ensemble_source_support_notes": 0,
            "ensemble_generated_support_notes": 0,
            "ensemble_echo_notes": 0,
            "ensemble_total_intervals": 0,
            "ensemble_max_poly": max_poly,
        }

    slots = support_slots(mapping)
    first_start = min(start for start, _, _ in melody_intervals)
    last_end = max(end for _, end, _ in melody_intervals)
    bar_start = (first_start // 16) * 16
    support: list[tuple[int, int, int]] = []
    echo: list[tuple[int, int, int]] = []
    support_steps: set[int] = set()
    source_support_notes = 0

    def add_support(step: int, duration: int, pitches: list[int]) -> int:
        if step < first_start or step >= last_end:
            return 0
        active = active_pitches_at(melody_intervals, step)
        available = max(0, max_poly - len(active))
        if available <= 0:
            return 0
        used: set[int] = set()
        added = 0
        for pitch in pitches[:available]:
            if pitch in active or pitch in used:
                continue
            support.append((step, min(total_steps, step + duration), pitch))
            used.add(pitch)
            support_steps.add(step)
            added += 1
        return added

    ordered = sorted(melody_intervals, key=lambda item: (item[0], item[1], item[2]))
    if ensemble_style == "full":
        beat = bar_start
        while beat < last_end:
            dense = melody_start_counts(melody_intervals, beat, beat + 4) >= 3
            phase = beat % 16
            if phase == 0:
                add_support(beat, 2, [slots["tonic"]] if dense else [slots["tonic"], slots["fifth"]])
            elif phase == 8:
                add_support(beat, 2, [slots["fifth"]] if dense else [slots["fifth"], slots["third"]])
            elif not dense:
                add_support(beat, 1, [slots["third"] if phase == 4 else slots["color"]])
            beat += 4
    elif ensemble_style == "light":
        bar = bar_start
        last_support = -999
        while bar < last_end:
            if bar >= first_start and melody_start_counts(melody_intervals, bar, bar + 16) <= 10:
                active = active_pitches_at(melody_intervals, bar)
                anchor = slots["tonic"] if (bar // 16) % 2 == 0 else slots["fifth"]
                if len(active) == 0:
                    add_support(bar, 2, [anchor, slots["third"]])
                else:
                    add_support(bar, 1, [anchor])
                last_support = bar
            bar += 16

        for idx, (_, end, pitch) in enumerate(ordered[:-1]):
            next_start = ordered[idx + 1][0]
            rest = next_start - end
            if rest < 8:
                continue
            step = end + min(4, max(1, rest // 2))
            if step - last_support < 12:
                continue
            add_support(step, min(2, max(1, rest - 1)), [harmony_echo_pitch(pitch, slots)])
            last_support = step
    else:
        by_source_step: dict[int, list[dict]] = defaultdict(list)
        for note in mapped:
            if note.get("is_raw_lead"):
                continue
            step = int(note["start_step"])
            if step < first_start or step >= last_end:
                continue
            if int(note["end_step"]) <= step:
                continue
            by_source_step[step].append(note)

        def source_support_score(note: dict, step: int) -> float:
            sound_pitch = int(note.get("sound_pitch", note["pitch"]))
            dur_steps = max(1, int(note["dur_steps"]))
            score = min(1.8, dur_steps / 6.0) + int(note.get("vel", 64)) / 150.0
            if not note.get("is_melody_track"):
                score += 1.3
            if note.get("is_top"):
                score += 0.4
            if step % 16 == 0:
                score += 1.0
            elif step % 8 == 0:
                score += 0.7
            elif step % 4 == 0:
                score += 0.35
            if sound_pitch <= 57:
                score += 0.8
            elif sound_pitch <= 62:
                score += 0.55
            elif sound_pitch <= 67:
                score += 0.25
            else:
                score -= 0.3
            score -= float(note.get("dist", 0.0)) * 0.08
            return score

        bar_counts: Counter[int] = Counter()
        last_support = -999
        for step in sorted(by_source_step):
            bar = step // 16
            bar_melody = melody_start_counts(melody_intervals, bar * 16, bar * 16 + 16)
            max_bar_support = 1
            if bar_counts[bar] >= max_bar_support:
                continue

            near_melody = melody_start_counts(melody_intervals, max(first_start, step - 4), min(last_end, step + 8))
            min_gap = 16 if near_melody >= 4 else 12
            if step - last_support < min_gap:
                continue
            if melody_start_counts(melody_intervals, step, step + 1) > 0:
                continue

            active = active_pitches_at(melody_intervals, step)
            if len(active) >= max_poly:
                continue
            candidates = [note for note in by_source_step[step] if int(note["pitch"]) not in active]
            if not candidates:
                continue

            chosen = max(candidates, key=lambda note: source_support_score(note, step))
            dur_steps = max(1, int(chosen["dur_steps"]))
            duration = 4 if dur_steps >= 8 else 3 if dur_steps >= 4 else 2
            added = add_support(step, duration, [int(chosen["pitch"])])
            if added:
                source_support_notes += added
                last_support = step
                bar_counts[bar] += added

        min_original_support = max(4, min(18, len(ordered) // 20))
        if source_support_notes < min_original_support:
            for idx, (_, end, pitch) in enumerate(ordered[:-1]):
                next_start = ordered[idx + 1][0]
                rest = next_start - end
                if rest < 12:
                    continue
                step = end + min(4, max(1, rest // 2))
                if step - last_support < 20 or any(abs(step - used_step) < 8 for used_step in support_steps):
                    continue
                added = add_support(step, 1, [harmony_echo_pitch(pitch, slots)])
                if added:
                    last_support = step
                if len(support) >= min_original_support:
                    break

    for idx, (start, end, pitch) in enumerate(ordered):
        if ensemble_style == "original":
            break
        next_start = ordered[idx + 1][0] if idx + 1 < len(ordered) else min(total_steps, start + 16)
        gap = next_start - start
        echo_start = start + 2
        if ensemble_style == "light":
            echo_start = end + 2
            if next_start - end < 12 or echo_start >= next_start or echo_start in support_steps:
                continue
        if gap < 6 or echo_start >= next_start or echo_start >= total_steps:
            continue
        echo_pitch = harmony_echo_pitch(pitch, slots)
        if echo_pitch in active_pitches_at(melody_intervals, echo_start):
            continue
        if ensemble_style == "light" and any(abs(echo_start - s) < 16 for s, _, _ in echo[-2:]):
            continue
        echo.append((echo_start, min(total_steps, echo_start + 1), echo_pitch))

    combined = base.merge_intervals_strict(melody_intervals + support + echo)
    return combined, {
        "ensemble_enabled": True,
        "ensemble_style": ensemble_style,
        "ensemble_support_notes": len(support),
        "ensemble_source_support_notes": source_support_notes,
        "ensemble_generated_support_notes": len(support) - source_support_notes,
        "ensemble_echo_notes": len(echo),
        "ensemble_total_intervals": len(combined),
        "ensemble_max_poly": max_poly,
        "ensemble_slots": {name: HANDPAN_NOTE_LABELS[HANDPAN_NOTES.index(pitch)] for name, pitch in slots.items()},
    }


def render_text(
    *,
    title: str,
    source: Path,
    mapping: dict[str, object],
    duration_s: float,
    initial_bpm: int,
    intervals: list[tuple[int, int, int]],
    total_steps: int,
    style: str,
    arrangement: str,
    max_poly: int,
) -> str:
    segments = base.intervals_to_segments_limited(intervals, total_steps, max_poly)
    lines = core.serialize_voice(segments, mapping["tempo_steps"])
    header = [
        f"Title:{title}",
        f"Source:{source}",
        "Info:kind=Sky8HandpanMelodyLock;layout=sky_handpan8;keys=YUIOPHJK;sound_range=D3-C5",
        f"Info:handpan_sounds={','.join(HANDPAN_NOTE_LABELS)};output=domiso_sky_handpan_compat",
        (
            f"Info:style={style};arrangement={arrangement};mapping={mapping['mapping_mode']};"
            f"max_poly={max_poly};"
            f"key={str(mapping['detected_key']).replace(' ', '_')};"
            f"range={mapping['contour_low']}-{mapping['contour_high']};"
            f"transpose={str(mapping['shift_summary']).replace(' ', '')}"
        ),
        f"Info:duration~{duration_s:.1f}s;grid=sixteenth;countin=none",
        "",
        f"bpm={initial_bpm}",
        "",
        ";Sky8HandpanMelodyLock",
    ]
    return "\n".join(header + lines).rstrip() + "\n"


def validate_intervals(intervals: list[tuple[int, int, int]], step_ms: list[float], total_steps: int) -> dict[str, object]:
    unmapped = sum(1 for _, _, pitch in intervals if pitch not in HANDPAN_NOTES)
    duration_ms = int(round(step_ms[min(total_steps, len(step_ms) - 1)])) if step_ms else 0
    return {
        "events": len(intervals),
        "diagnostics": 0,
        "unmapped": unmapped,
        "duration_ms": duration_ms,
    }


def next_output_paths(out_dir: Path, midi_stem: str) -> tuple[Path, Path, int]:
    safe_base = core.normalize_output_base(midi_stem)
    song_dir = out_dir / safe_base
    song_dir.mkdir(parents=True, exist_ok=True)
    txt_prefix = f"{safe_base}_domiso_script_sky8_handpan_melodylock_v"
    report_prefix = f"{safe_base}_analysis_sky8_handpan_melodylock_v"
    max_version = 0
    for child in song_dir.iterdir():
        name = child.name
        if name.startswith(txt_prefix) and name.endswith(".txt"):
            version_text = name.removeprefix(txt_prefix).removesuffix(".txt")
        elif name.startswith(report_prefix) and name.endswith(".md"):
            version_text = name.removeprefix(report_prefix).removesuffix(".md")
        else:
            version_text = ""
        if version_text.isdigit():
            max_version = max(max_version, int(version_text))
    version = max_version + 1
    txt_path = song_dir / f"{safe_base}_domiso_script_sky8_handpan_melodylock_v{version}.txt"
    report_path = song_dir / f"{safe_base}_analysis_sky8_handpan_melodylock_v{version}.md"
    return txt_path, report_path, version


def write_report(
    path: Path,
    *,
    input_path: Path,
    version: int,
    style: str,
    mapping: dict[str, object],
    stats: dict[str, object],
    validation: dict[str, object],
    txt_path: Path,
    duration_s: float,
) -> None:
    shifts = mapping["shifts"]
    lines = [
        f"# Analysis (Sky8 Handpan MelodyLock): {input_path.name}",
        "",
        "## Layout",
        f"- layout: sky8_handpan",
        f"- keys: {HANDPAN_LAYOUT}",
        f"- sounds: {HANDPAN_NOTE_INFO}",
        "- output_pitches: Domiso Sky Handpan compatibility map, unchanged software key slots",
        "",
        "## Mapping",
        f"- version: {version}",
        f"- style: {style}",
        f"- arrangement: {stats.get('arrangement_style', '')}",
        f"- mapping_mode: {mapping['mapping_mode']}",
        f"- detected_key: {mapping['detected_key']}",
        f"- detected_key_score: {mapping['detected_key_score']}",
        f"- key_shift_target_pentatonic_tonic: {mapping['key_shift_target']}",
        f"- contour_range: {mapping['contour_low']}..{mapping['contour_high']}",
        f"- lead_mapping_index_counts: {mapping['lead_mapping_index_counts']}",
        f"- lead_mapping_total_dist: {mapping['lead_mapping_total_dist']}",
        f"- base_shift: {mapping['base_shift']}",
        f"- dynamic_windows: {mapping['shift_summary']}",
        f"- shift_changes: {mapping['shift_changes']}",
        f"- window_count: {len(shifts)}",
        f"- duration_s: {duration_s:.2f}",
        "",
        "## Counts",
        *[f"- {key}: {value}" for key, value in stats.items()],
        "",
        "## Validation",
        *[f"- {key}: {value}" for key, value in validation.items()],
        "",
        "## Output",
        f"- txt: {txt_path}",
        "",
        "## Use",
        "- In Domiso, select Game = Sky Handpan before playing this TXT.",
        "- The TXT only uses notes mapped to Y U I O P H J K.",
        "- No Domiso software profile change is required; output pitches intentionally use the existing key-slot map.",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def run(
    input_midi: Path,
    out_dir: Path,
    style: str,
    mapping_mode: str,
    *,
    preferred_lead_track: int | None = None,
    blend_lead_tracks: bool = False,
    arrangement_style: str = "short",
    ensemble_style: str = "off",
) -> tuple[Path, Path, dict[str, object]]:
    parsed = core.parse_midi(str(input_midi))
    if not parsed["notes"]:
        raise ValueError("MIDI contains no notes")
    if preferred_lead_track is not None:
        known_tracks = {int(note["track"]) for note in parsed["notes"]}
        if preferred_lead_track not in known_tracks:
            raise ValueError(f"lead track {preferred_lead_track} not found; available tracks: {sorted(known_tracks)}")
    preset = STYLE_PRESETS[style]
    mapped, mapping = map_notes(
        parsed,
        mapping_mode,
        preferred_lead_track=preferred_lead_track,
        blend_lead_tracks=blend_lead_tracks,
    )
    total_steps = max(int(note["end_step"]) for note in mapped) + 1
    step_ms = build_step_ms(total_steps, mapping["tempo_steps"])
    if arrangement_style == "literal":
        intervals, stats = build_literal_source_intervals(mapped)
        ensemble_stats = {
            "ensemble_enabled": False,
            "ensemble_style": "off",
            "ensemble_support_notes": 0,
            "ensemble_source_support_notes": 0,
            "ensemble_generated_support_notes": 0,
            "ensemble_echo_notes": 0,
            "ensemble_total_intervals": len(intervals),
            "ensemble_max_poly": SOURCE_LITERAL_MAX_POLY,
        }
        max_poly = SOURCE_LITERAL_MAX_POLY
    elif arrangement_style == "short":
        melody_intervals, stats = build_melody_intervals(mapped, int(mapping["melody_track"]), preset, step_ms)
        intervals, short_stats = build_short_tail_intervals(melody_intervals, mapped, total_steps)
        stats = {**stats, **short_stats}
        ensemble_stats = {
            "ensemble_enabled": False,
            "ensemble_style": "off",
            "ensemble_support_notes": int(short_stats["short_tail_support_notes"]),
            "ensemble_source_support_notes": int(short_stats["short_tail_support_notes"]),
            "ensemble_generated_support_notes": 0,
            "ensemble_echo_notes": 0,
            "ensemble_total_intervals": len(intervals),
            "ensemble_max_poly": SHORT_ADAPTED_MAX_POLY,
        }
        max_poly = SHORT_ADAPTED_MAX_POLY
    else:
        melody_intervals, stats = build_melody_intervals(mapped, int(mapping["melody_track"]), preset, step_ms)
        if ensemble_style != "off":
            intervals, ensemble_stats = build_ensemble_intervals(melody_intervals, mapped, total_steps, mapping, ensemble_style)
            max_poly = ENSEMBLE_MAX_POLY[ensemble_style]
        else:
            intervals = melody_intervals
            ensemble_stats = {
                "ensemble_enabled": False,
                "ensemble_style": "off",
                "ensemble_support_notes": 0,
                "ensemble_source_support_notes": 0,
                "ensemble_generated_support_notes": 0,
                "ensemble_echo_notes": 0,
                "ensemble_total_intervals": len(intervals),
                "ensemble_max_poly": ENSEMBLE_MAX_POLY["off"],
            }
            max_poly = ENSEMBLE_MAX_POLY["off"]
    extract_stats = {f"extract_{key}": value for key, value in dict(mapping["lead_stats"]).items()}
    stats = {"arrangement_style": arrangement_style, **extract_stats, **stats, **ensemble_stats}
    tempos = mapping["tempos"]
    duration_s = core.tick_to_seconds(parsed["max_tick"], tempos, parsed["tpb"])
    initial_bpm = int(round(tempos[0][1])) if tempos else 120
    txt_path, report_path, version = next_output_paths(out_dir, input_midi.stem)
    text = render_text(
        title=f"{input_midi.stem} sky8 handpan melodylock v{version}",
        source=input_midi,
        mapping=mapping,
        duration_s=duration_s,
        initial_bpm=initial_bpm,
        intervals=intervals,
        total_steps=total_steps,
        style=style,
        arrangement=arrangement_style,
        max_poly=max_poly,
    )
    validation = validate_intervals(intervals, step_ms, total_steps)
    if validation["diagnostics"] or validation["unmapped"]:
        raise RuntimeError(f"validation failed: {validation}")
    txt_path.write_text(text, encoding="utf-8")
    write_report(
        report_path,
        input_path=input_midi,
        version=version,
        style=style,
        mapping=mapping,
        stats=stats,
        validation=validation,
        txt_path=txt_path,
        duration_s=duration_s,
    )
    return txt_path, report_path, validation


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Sky 8-key handpan melodylock Domiso TXT.")
    parser.add_argument("cmd_or_input", nargs="?", help="MIDI path, or 'pipeline' for Domiso MIDI generator compatibility.")
    parser.add_argument("pipeline_input_midi", nargs="?", help="MIDI path when using the pipeline subcommand.")
    parser.add_argument("--out-dir", default=str(ROOT_DIR / "txt"))
    parser.add_argument("--report-dir", default="")
    parser.add_argument("--profile", default="auto", help="Accepted for compatibility; ignored.")
    parser.add_argument("--style", choices=sorted(STYLE_PRESETS), default="balanced")
    parser.add_argument(
        "--mapping",
        choices=["literal", "keyshift", "contour", "scale", "snap"],
        default="literal",
        help=(
            "literal preserves source MIDI timing/tracks and only snaps each pitch to the nearest handpan key; "
            "contour preserves hook height on 8 keys; "
            "keyshift globally transposes detected keys toward the real Sky handpan pentatonic set; "
            "scale uses legacy degree mapping; "
            "snap is the dynamic nearest-handpan-note quantizer."
        ),
    )
    parser.add_argument(
        "--arrangement",
        choices=["short", "literal", "melodylock"],
        default="short",
        help=(
            "short is the default for the short Sky handpan sound: lead taps, sparse source support, max two keys; "
            "literal keeps all mapped source notes; melodylock uses the older lead-focused arranger."
        ),
    )
    parser.add_argument("--lead-track", default="auto", help="Force a MIDI note track number for the handpan melody.")
    parser.add_argument(
        "--blend-lead-tracks",
        action="store_true",
        help="Allow the legacy behavior that mixes multiple lead-like tracks.",
    )
    parser.add_argument(
        "--ensemble-style",
        choices=["original", "light", "full", "off"],
        default="off",
        help="For non-literal melodylock modes only: original/light/full add progressively stronger handpan support.",
    )
    parser.add_argument("--no-ensemble", action="store_true", help="Alias for --ensemble-style off.")
    parser.add_argument("--latest-download", action="store_true", help="Force using the latest MIDI in Downloads.")
    args = parser.parse_args()

    if args.cmd_or_input == "pipeline":
        if not args.pipeline_input_midi:
            raise SystemExit("pipeline input_midi is required")
        input_midi = Path(args.pipeline_input_midi)
    elif args.latest_download or not args.cmd_or_input:
        input_midi = latest_downloads_midi()
    else:
        input_midi = Path(args.cmd_or_input)
    if str(args.lead_track).lower() == "auto":
        preferred_lead_track = None
    else:
        preferred_lead_track = int(args.lead_track)
    ensemble_style = "off" if args.no_ensemble else args.ensemble_style
    txt_path, report_path, validation = run(
        input_midi,
        Path(args.out_dir),
        args.style,
        args.mapping,
        preferred_lead_track=preferred_lead_track,
        blend_lead_tracks=bool(args.blend_lead_tracks),
        arrangement_style=args.arrangement,
        ensemble_style=ensemble_style,
    )
    print(f"input={input_midi}")
    print(f"txt={txt_path}")
    print(f"report={report_path}")
    print(f"validation={validation}")


if __name__ == "__main__":
    main()
