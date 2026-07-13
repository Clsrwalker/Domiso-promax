#!/usr/bin/env python3
"""
Convert a MIDI file into a Sky DJ 4x4x8 grid text.

The output is a visual grid, not a Domiso playback score:
- 4 instruments/layers
- fixed layer roles: piano, violin, percussion, flute
- each layer has 4 bars by default
- each bar has 4 rows
- each row has 8 time slots, played left to right
- each cell is one note value 1..7, or 0 for a rest
"""

from __future__ import annotations

import argparse
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import mido
except ImportError as exc:  # pragma: no cover - user-facing CLI guard
    raise SystemExit("Missing dependency: mido. Install with: pip install mido") from exc


PC_NAMES = {
    "C": 0,
    "C#": 1,
    "DB": 1,
    "D": 2,
    "D#": 3,
    "EB": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "GB": 6,
    "G": 7,
    "G#": 8,
    "AB": 8,
    "A": 9,
    "A#": 10,
    "BB": 10,
    "B": 11,
}

MAJOR_INTERVALS = [0, 2, 4, 5, 7, 9, 11]
MINOR_INTERVALS = [0, 2, 3, 5, 7, 8, 10]

KRUMHANSL_MAJOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KRUMHANSL_MINOR = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
SLOTS_PER_ROW = 8


@dataclass(frozen=True)
class Note:
    start: int
    end: int
    pitch: int
    velocity: int
    channel: int
    track: int


def normalize_tonic(value: str) -> int:
    key = value.strip().upper().replace("♭", "B").replace("♯", "#")
    if key not in PC_NAMES:
        raise argparse.ArgumentTypeError(f"Unsupported tonic: {value}")
    return PC_NAMES[key]


def collect_midi(path: Path) -> tuple[mido.MidiFile, list[Note], int, tuple[int, int]]:
    midi = mido.MidiFile(path)
    tempo = 500000
    time_sig = (4, 4)
    notes: list[Note] = []

    meta_seen = False
    for track_index, track in enumerate(midi.tracks):
        tick = 0
        active: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
        for msg in track:
            tick += msg.time
            if msg.type == "set_tempo" and not meta_seen:
                tempo = msg.tempo
            elif msg.type == "time_signature" and time_sig == (4, 4):
                time_sig = (msg.numerator, msg.denominator)

            if msg.type == "note_on" and msg.velocity > 0:
                active[(msg.channel, msg.note)].append((tick, msg.velocity))
            elif msg.type in ("note_off", "note_on") and hasattr(msg, "note"):
                key = (msg.channel, msg.note)
                if active[key]:
                    start, velocity = active[key].pop(0)
                    if tick > start:
                        notes.append(Note(start, tick, msg.note, velocity, msg.channel, track_index))
        meta_seen = meta_seen or track_index == 0

    return midi, notes, tempo, time_sig


def weighted_pitch_class_hist(notes: Iterable[Note]) -> list[float]:
    hist = [0.0] * 12
    for note in notes:
        weight = max(1, note.end - note.start) * max(1, note.velocity)
        hist[note.pitch % 12] += weight
    return hist


def rotated_profile_score(hist: list[float], tonic: int, profile: list[float]) -> float:
    return sum(hist[(tonic + i) % 12] * profile[i] for i in range(12))


def infer_key(notes: list[Note], tonic_override: int | None, scale_override: str) -> tuple[int, str]:
    hist = weighted_pitch_class_hist(notes)
    if tonic_override is not None:
        if scale_override != "auto":
            return tonic_override, scale_override
        major_score = rotated_profile_score(hist, tonic_override, KRUMHANSL_MAJOR)
        minor_score = rotated_profile_score(hist, tonic_override, KRUMHANSL_MINOR)
        return tonic_override, "minor" if minor_score > major_score else "major"

    best: tuple[float, int, str] | None = None
    scales = ["major", "minor"] if scale_override == "auto" else [scale_override]
    for tonic in range(12):
        for scale in scales:
            profile = KRUMHANSL_MINOR if scale == "minor" else KRUMHANSL_MAJOR
            score = rotated_profile_score(hist, tonic, profile)
            if best is None or score > best[0]:
                best = (score, tonic, scale)
    assert best is not None
    return best[1], best[2]


def circular_distance(a: int, b: int) -> int:
    diff = abs((a - b) % 12)
    return min(diff, 12 - diff)


def pitch_to_degree(pitch: int, tonic: int, scale: str, high_threshold: float) -> tuple[int, bool]:
    intervals = MINOR_INTERVALS if scale == "minor" else MAJOR_INTERVALS
    rel = (pitch % 12 - tonic) % 12
    best_index = 0
    best_distance = 99
    for idx, interval in enumerate(intervals):
        dist = circular_distance(rel, interval)
        if dist < best_distance:
            best_index = idx
            best_distance = dist
    degree = best_index + 1
    high_one = degree == 1 and pitch >= high_threshold
    return degree, high_one


def notes_starting_in(notes: list[Note], start: float, end: float) -> list[Note]:
    return [note for note in notes if start <= note.start < end]


def notes_sounding_in(notes: list[Note], start: float, end: float) -> list[Note]:
    return [note for note in notes if note.start < end and note.end > start]


def mask_from_pitches(
    pitches: Iterable[int],
    tonic: int,
    scale: str,
    high_threshold: float,
    max_hits: int,
) -> list[str]:
    cells = ["0"] * 8
    used = set()
    for pitch in pitches:
        degree, high_one = pitch_to_degree(pitch, tonic, scale, high_threshold)
        col = 7 if high_one else degree - 1
        if col in used:
            continue
        cells[col] = "1" if col == 7 else str(degree)
        used.add(col)
        if len(used) >= max_hits:
            break
    return cells


def unique_by_degree(
    notes: Iterable[Note],
    tonic: int,
    scale: str,
    high_threshold: float,
    reverse_pitch: bool,
) -> list[int]:
    result: list[int] = []
    seen = set()
    ordered = sorted(notes, key=lambda n: (n.pitch, n.velocity), reverse=reverse_pitch)
    for note in ordered:
        degree, high_one = pitch_to_degree(note.pitch, tonic, scale, high_threshold)
        key = (degree, high_one)
        if key in seen:
            continue
        seen.add(key)
        result.append(note.pitch)
    return result


def exclude_same_degrees(
    pitches: Iterable[int],
    excluded: Iterable[int],
    tonic: int,
    scale: str,
    high_threshold: float,
) -> list[int]:
    excluded_keys = {
        pitch_to_degree(pitch, tonic, scale, high_threshold)
        for pitch in excluded
        if pitch is not None
    }
    result: list[int] = []
    seen = set()
    for pitch in pitches:
        key = pitch_to_degree(pitch, tonic, scale, high_threshold)
        if key in excluded_keys or key in seen:
            continue
        seen.add(key)
        result.append(pitch)
    return result


def percussion_mask(starting: list[Note], sounding: list[Note], row: int) -> list[str]:
    cells = ["0"] * 8
    drum_notes = [n for n in starting if n.channel == 9]
    if not drum_notes:
        drum_notes = [n for n in sounding if n.channel == 9]

    if drum_notes:
        for note in sorted(drum_notes, key=lambda n: (n.start, n.pitch)):
            pitch = note.pitch
            if pitch in (35, 36):  # kick
                col = 0
            elif pitch in (37, 38, 39, 40):  # snare/clap/rim
                col = 4
            elif pitch in (42, 44, 46):  # hats
                col = 6
            elif pitch in (49, 51, 52, 55, 57):  # crash/ride
                col = 7
            else:
                col = pitch % 8
            cells[col] = "1" if col == 7 else str(col + 1)
        return cells

    # No drum channel: generate a sparse DJ pulse. Keep rows 2/4 empty so the
    # grid preserves rests instead of becoming a constant stream.
    if row == 0:
        cells[0] = "1"
    elif row == 2:
        cells[0] = "1"
        cells[4] = "5"
    return cells


def non_drum(notes: Iterable[Note]) -> list[Note]:
    return [note for note in notes if note.channel != 9]


def row_windows(start_tick: float, bar_ticks: float, bars: int, rows: int) -> list[tuple[int, int, float, float]]:
    row_ticks = bar_ticks / rows
    windows = []
    for bar in range(bars):
        for row in range(rows):
            s = start_tick + bar * bar_ticks + row * row_ticks
            windows.append((bar, row, s, s + row_ticks))
    return windows


def quantile_pitch(notes: list[Note], fraction: float, fallback: int) -> int:
    pitches = sorted(note.pitch for note in notes)
    if not pitches:
        return fallback
    index = max(0, min(len(pitches) - 1, int(len(pitches) * fraction)))
    return pitches[index]


def best_melody_pitch(
    row_notes: list[Note],
    sounding: list[Note],
    median_pitch: int,
    prev_pitch: int | None,
    allow_sustain: bool = False,
) -> int | None:
    candidates = [n for n in non_drum(row_notes) if n.pitch >= median_pitch - 2]
    if not candidates and allow_sustain:
        candidates = [n for n in non_drum(sounding) if n.pitch >= median_pitch - 2]
    if not candidates:
        candidates = non_drum(row_notes)
    if not candidates and allow_sustain:
        candidates = non_drum(sounding)
    if not candidates:
        return None

    def score(note: Note) -> float:
        duration = max(1, note.end - note.start)
        continuity = 0 if prev_pitch is None else abs(note.pitch - prev_pitch)
        return note.pitch * 1.4 + note.velocity * 0.2 + min(duration, 960) * 0.01 - continuity * 0.35

    return max(candidates, key=score).pitch


def row_degree_key(pitch: int, tonic: int, scale: str, high_threshold: float) -> tuple[int, bool]:
    return pitch_to_degree(pitch, tonic, scale, high_threshold)


def melody_sequence_for_window(
    notes: list[Note],
    start_tick: float,
    bar_ticks: float,
    bars: int,
    rows: int,
) -> list[int | None]:
    window_notes = [
        n
        for n in non_drum(notes)
        if start_tick <= n.start < start_tick + bars * bar_ticks
        or (n.start < start_tick + bars * bar_ticks and n.end > start_tick)
    ]
    median_pitch = quantile_pitch(window_notes, 0.55, 64)
    seq: list[int | None] = []
    prev_pitch: int | None = None
    for _bar, _row, s, e in row_windows(start_tick, bar_ticks, bars, rows):
        starting = notes_starting_in(window_notes, s, e)
        sounding = notes_sounding_in(window_notes, s, e)
        pitch = best_melody_pitch(starting, sounding, median_pitch, prev_pitch, allow_sustain=False)
        seq.append(pitch)
        if pitch is not None:
            prev_pitch = pitch
    return seq


def hook_score_for_window(
    notes: list[Note],
    start_tick: float,
    bar_ticks: float,
    bars: int,
    rows: int,
    tonic: int,
    scale: str,
) -> float:
    end_tick = start_tick + bars * bar_ticks
    window_notes = [n for n in non_drum(notes) if start_tick <= n.start < end_tick]
    if not window_notes:
        return -9999.0

    high_threshold = quantile_pitch(window_notes, 0.70, 72)
    seq = melody_sequence_for_window(notes, start_tick, bar_ticks, bars, rows)
    active = sum(p is not None for p in seq)
    if active < max(4, rows):
        return -200.0 + active

    degrees = [
        row_degree_key(p, tonic, scale, high_threshold)
        for p in seq
        if p is not None
    ]
    distinct = len(set(degrees))
    pitch_values = [p for p in seq if p is not None]
    pitch_range = max(pitch_values) - min(pitch_values) if pitch_values else 0
    density = len(window_notes) / max(1, bars * rows)

    longest_run = 1
    current_run = 1
    last_key = None
    for key in degrees:
        if key == last_key:
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 1
            last_key = key

    empty = len(seq) - active
    score = 0.0
    score += active * 2.5
    score += distinct * 6.0
    score += min(pitch_range, 18) * 0.8
    score -= empty * 2.0
    score -= max(0.0, density - 6.0) * 4.0
    score -= max(0, longest_run - 4) * 5.0
    return score


def melody_signature_for_window(
    notes: list[Note],
    start_tick: float,
    bar_ticks: float,
    bars: int,
    rows: int,
    tonic: int,
    scale: str,
) -> tuple[str, ...]:
    end_tick = start_tick + bars * bar_ticks
    window_notes = [n for n in non_drum(notes) if start_tick <= n.start < end_tick]
    high_threshold = quantile_pitch(window_notes, 0.70, 72)
    seq = melody_sequence_for_window(notes, start_tick, bar_ticks, bars, rows)
    signature: list[str] = []
    for pitch in seq:
        if pitch is None:
            signature.append("0")
            continue
        degree, high_one = pitch_to_degree(pitch, tonic, scale, high_threshold)
        signature.append("8" if high_one else str(degree))
    return tuple(signature)


def build_row_time_layers(
    notes: list[Note],
    start_tick: float,
    bar_ticks: float,
    bars: int,
    rows: int,
    tonic: int,
    scale: str,
    max_chord_notes: int,
) -> dict[str, list[list[str]]]:
    end_tick = start_tick + bars * bar_ticks
    window_notes = [
        note
        for note in notes
        if start_tick <= note.start < end_tick
        or (note.start < end_tick and note.end > start_tick)
    ]
    high_threshold = quantile_pitch(window_notes, 0.65, 72)
    median_pitch = quantile_pitch(non_drum(window_notes), 0.55, 64)

    layers: dict[str, list[list[str]]] = {
        "乐器1 钢琴主旋律": [],
        "乐器2 小提琴和声": [],
        "乐器3 打击乐": [],
        "乐器4 笛子点缀": [],
    }

    prev_melody_pitch: int | None = None
    for bar, row, s, e in row_windows(start_tick, bar_ticks, bars, rows):
        starting = notes_starting_in(notes, s, e)
        pitched_starting = non_drum(starting)

        melody_pitch = best_melody_pitch(
            pitched_starting,
            [],
            median_pitch,
            prev_melody_pitch,
            allow_sustain=False,
        )
        if melody_pitch is not None:
            prev_melody_pitch = melody_pitch

        high_notes = [n for n in pitched_starting if n.pitch >= median_pitch]
        low_notes = [n for n in pitched_starting if n.pitch < median_pitch]
        high_unique = unique_by_degree(high_notes, tonic, scale, high_threshold, True)
        low_unique = unique_by_degree(low_notes, tonic, scale, high_threshold, False)
        all_unique = unique_by_degree(pitched_starting, tonic, scale, high_threshold, False)

        piano_pitches = [melody_pitch] if melody_pitch is not None else []
        harmony_pool = low_unique or all_unique
        violin_pitches = exclude_same_degrees(
            harmony_pool,
            piano_pitches,
            tonic,
            scale,
            high_threshold,
        )[:max_chord_notes]
        flute_pitches = exclude_same_degrees(
            high_unique,
            piano_pitches,
            tonic,
            scale,
            high_threshold,
        )[:1]

        layers["乐器1 钢琴主旋律"].append(mask_from_pitches(piano_pitches, tonic, scale, high_threshold, 1))
        layers["乐器2 小提琴和声"].append(mask_from_pitches(violin_pitches, tonic, scale, high_threshold, max_chord_notes))
        layers["乐器3 打击乐"].append(percussion_mask(starting, starting, row))
        layers["乐器4 笛子点缀"].append(mask_from_pitches(flute_pitches, tonic, scale, high_threshold, 1))

    return layers


def infer_grid_bpm(tempo_us: int, ticks_per_beat: int, bar_ticks: float, rows: int) -> int:
    row_ticks = bar_ticks / rows
    row_ms = (tempo_us / 1000.0) * (row_ticks / ticks_per_beat)
    if row_ms <= 0:
        return 120
    return int(round(60000.0 / row_ms))


def infer_row_ms(tempo_us: int, ticks_per_beat: int, bar_ticks: float, rows: int) -> int:
    row_ticks = bar_ticks / rows
    return max(1, int(round((tempo_us / 1000.0) * (row_ticks / ticks_per_beat))))


def find_hook_starts(
    notes: list[Note],
    bar_ticks: float,
    bars: int,
    rows: int,
    tonic: int,
    scale: str,
    limit: int,
) -> list[tuple[int, float]]:
    if not notes:
        return [(1, 0.0)]
    max_bar = max(1, int(math.ceil(max(n.end for n in notes) / bar_ticks)) - bars + 1)
    scored: list[tuple[int, float]] = []
    for start_bar in range(1, max_bar + 1):
        start_tick = (start_bar - 1) * bar_ticks
        score = hook_score_for_window(notes, start_tick, bar_ticks, bars, rows, tonic, scale)
        if score > -1000:
            scored.append((start_bar, score))
    if not scored:
        return [(1, 0.0)]

    scored.sort(key=lambda item: item[1], reverse=True)
    chosen: list[tuple[int, float]] = []
    seen_signatures: set[tuple[str, ...]] = set()
    for start_bar, score in scored:
        start_tick = (start_bar - 1) * bar_ticks
        signature = melody_signature_for_window(notes, start_tick, bar_ticks, bars, rows, tonic, scale)
        if signature in seen_signatures:
            continue
        if not all(abs(start_bar - existing) >= bars for existing, _score in chosen):
            continue
        seen_signatures.add(signature)
        chosen.append((start_bar, score))
        if len(chosen) >= limit:
            break
    return chosen or [scored[0]]


def output_for_candidate(base_output: Path, index: int, total: int) -> Path:
    if total <= 1:
        return base_output
    return base_output.with_name(f"{base_output.stem}_candidate{index}{base_output.suffix}")


def clean_title(path: Path, title: str | None) -> str:
    if title:
        return title
    name = re.sub(r"[_-]+", " ", path.stem).strip()
    return re.sub(r"\s+", " ", name).title() or path.stem


def format_layers_block(
    label: str,
    start_bar: int,
    bars: int,
    layers: dict[str, list[list[str]]],
    rows_per_bar: int,
) -> list[str]:
    lines: list[str] = [
        label,
        f"小节范围: {start_bar}-{start_bar + bars - 1}",
        "",
    ]
    for layer_name, rows in layers.items():
        lines.append(layer_name)
        for bar_index in range(bars):
            lines.append(f"小节{bar_index + 1}")
            start = bar_index * rows_per_bar
            for row in rows[start : start + rows_per_bar]:
                lines.append(" ".join(row))
            lines.append("")
    return lines


def timing_lines(bpm: int, bars: int, rows_per_bar: int, row_ms: int) -> list[str]:
    fragment_rows = bars * rows_per_bar
    fragment_ms = row_ms * fragment_rows
    return [
        f"行间隔ms: {row_ms}",
        "播放规则: 每行是一个时间步；8 列是音位；整行 0 是空拍",
        f"每小节行数: {rows_per_bar}",
        f"每行列数: {SLOTS_PER_ROW}",
        f"每片段行数: {fragment_rows}",
        f"每片段时长ms: {fragment_ms}",
    ]


def format_single_output(
    title: str,
    source: Path,
    bpm: int,
    candidates: list[dict],
    rows_per_bar: int,
    row_ms: int,
) -> str:
    lines: list[str] = [
        title,
        "Sky DJ 行时间格 hook fragments v7",
        f"建议速度: {bpm}",
        f"来源: {source.name}",
        "",
        "列: 1 2 3 4 5 6 7 1",
        "0 = 空；整行 0 = 这个时间步不弹",
        *timing_lines(bpm, candidates[0]["bars"] if candidates else 4, rows_per_bar, row_ms),
        "",
        "乐器1 钢琴主旋律",
        "乐器2 小提琴和声",
        "乐器3 打击乐",
        "乐器4 笛子点缀",
        "",
    ]
    for index, candidate in enumerate(candidates, 1):
        label = f"片段{index} hook_score={candidate['score']:.1f}"
        lines.extend(format_layers_block(label, candidate["start_bar"], candidate["bars"], candidate["layers"], rows_per_bar))
    return "\n".join(lines).rstrip() + "\n"


def format_split_output(
    title: str,
    source: Path,
    bpm: int,
    candidate: dict,
    rows_per_bar: int,
    row_ms: int,
) -> str:
    lines: list[str] = [
        title,
        "Sky DJ 行时间格 hook fragments v7",
        f"建议速度: {bpm}",
        f"来源: {source.name}",
        "",
        "列: 1 2 3 4 5 6 7 1",
        "0 = 空；整行 0 = 这个时间步不弹",
        *timing_lines(bpm, candidate["bars"], rows_per_bar, row_ms),
        "",
    ]
    lines.extend(format_layers_block("片段1", candidate["start_bar"], candidate["bars"], candidate["layers"], rows_per_bar))
    return "\n".join(lines).rstrip() + "\n"


def format_output(
    title: str,
    source: Path,
    bpm: int,
    start_bar: int,
    bars: int,
    layers: dict[str, list[list[str]]],
    row_ms: int = 0,
) -> str:
    if row_ms <= 0:
        row_ms = max(1, int(round(60000.0 / max(1, bpm))))
    lines: list[str] = [
        title,
        "Sky DJ 行时间格 hook fragments v7",
        f"建议速度: {bpm}",
        f"来源: {source.name}",
        "",
        "列: 1 2 3 4 5 6 7 1",
        "0 = 空；整行 0 = 这个时间步不弹",
        *timing_lines(bpm, bars, 4, row_ms),
        "",
    ]
    rows_per_bar = 4
    lines.extend(format_layers_block("片段1", start_bar, bars, layers, rows_per_bar))
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert MIDI to Sky DJ 4x4x8 grid txt.")
    parser.add_argument("midi", type=Path, help="Input MIDI file")
    parser.add_argument("-o", "--output", type=Path, help="Output txt path")
    parser.add_argument("--title", help="Title written to the txt")
    parser.add_argument("--start-bar", type=int, help="1-based bar to start from; default auto-picks a hook")
    parser.add_argument("--auto-start", action="store_true", help="Force auto-pick a hook section")
    parser.add_argument("--candidates", type=int, default=6, help="Include the top N unique hook fragments")
    parser.add_argument("--split-candidates", action="store_true", help="Write each fragment to a separate file")
    parser.add_argument("--bars", type=int, default=4, help="Number of bars to export")
    parser.add_argument("--rows", type=int, default=4, help="Rows per bar")
    parser.add_argument("--bpm", type=int, help="Override suggested grid BPM")
    parser.add_argument("--tonic", type=normalize_tonic, help="Tonic, e.g. C, F#, Bb")
    parser.add_argument("--scale", choices=["auto", "major", "minor"], default="auto")
    parser.add_argument("--max-chord-notes", type=int, default=3, help="Max hits in harmony rows")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bars <= 0 or args.rows <= 0:
        raise SystemExit("--bars and --rows must be positive")
    if args.max_chord_notes < 1 or args.max_chord_notes > 8:
        raise SystemExit("--max-chord-notes must be between 1 and 8")
    if args.candidates < 1:
        raise SystemExit("--candidates must be positive")

    midi, notes, tempo_us, time_sig = collect_midi(args.midi)
    numerator, denominator = time_sig
    bar_ticks = midi.ticks_per_beat * numerator * (4.0 / denominator)
    bpm = args.bpm or infer_grid_bpm(tempo_us, midi.ticks_per_beat, bar_ticks, args.rows)
    if args.bpm:
        row_ms = max(1, int(round(60000.0 / bpm)))
    else:
        row_ms = infer_row_ms(tempo_us, midi.ticks_per_beat, bar_ticks, args.rows)

    output = args.output
    if output is None:
        output = args.midi.with_name(args.midi.stem + "_sky_dj_grid_auto_v1.txt")
    output.parent.mkdir(parents=True, exist_ok=True)

    if args.start_bar is not None and not args.auto_start:
        start_bars = [(args.start_bar, 0.0)]
        key_notes = [n for n in notes if (args.start_bar - 1) * bar_ticks <= n.start < (args.start_bar - 1 + args.bars) * bar_ticks]
        tonic, scale = infer_key(key_notes or notes, args.tonic, args.scale)
    else:
        tonic, scale = infer_key(notes, args.tonic, args.scale)
        start_bars = find_hook_starts(notes, bar_ticks, args.bars, args.rows, tonic, scale, args.candidates)

    candidates = []
    for index, (start_bar, score) in enumerate(start_bars, 1):
        start_tick = (start_bar - 1) * bar_ticks
        window_notes = [n for n in notes if start_tick <= n.start < start_tick + args.bars * bar_ticks]
        candidate_tonic, candidate_scale = infer_key(window_notes or notes, args.tonic, args.scale)
        layers = build_row_time_layers(
            notes,
            start_tick,
            bar_ticks,
            args.bars,
            args.rows,
            candidate_tonic,
            candidate_scale,
            args.max_chord_notes,
        )
        candidates.append(
            {
                "start_bar": start_bar,
                "score": score,
                "bars": args.bars,
                "layers": layers,
                "tonic": candidate_tonic,
                "scale": candidate_scale,
            }
        )

    title = clean_title(args.midi, args.title)
    written = []
    if args.split_candidates:
        for index, candidate in enumerate(candidates, 1):
            text = format_split_output(title, args.midi, bpm, candidate, args.rows, row_ms)
            out_path = output_for_candidate(output, index, len(candidates))
            out_path.write_text(text, encoding="utf-8")
            written.append(out_path)
            score = candidate["score"]
            quality = "low_hook_score" if score and score < 45 else "ok"
            print(
                f"Wrote {out_path} | start_bar={candidate['start_bar']} "
                f"hook_score={score:.1f} quality={quality} "
                f"key_pc={candidate['tonic']} scale={candidate['scale']}"
            )
    else:
        text = format_single_output(title, args.midi, bpm, candidates, args.rows, row_ms)
        output.write_text(text, encoding="utf-8")
        written.append(output)
        starts = ", ".join(str(candidate["start_bar"]) for candidate in candidates)
        print(f"Wrote {output} | fragments={len(candidates)} start_bars={starts}")
        for candidate in candidates:
            score = candidate["score"]
            quality = "low_hook_score" if score and score < 45 else "ok"
            print(
                f"  fragment start_bar={candidate['start_bar']} "
                f"hook_score={score:.1f} quality={quality} "
                f"key_pc={candidate['tonic']} scale={candidate['scale']}"
            )

    print(f"Suggested BPM={bpm}; fragments={len(candidates)}; files={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
