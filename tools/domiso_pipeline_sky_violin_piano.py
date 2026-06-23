#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import statistics
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import mido

TOOLS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TOOLS_DIR.parent
ORCHESTRA_DIR = ROOT_DIR / "Domiso-Orchestra"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import midi_to_domiso_dense3layer as core
import domiso_pipeline_literal as base
import domiso_pipeline_sky_melodylock as sky


SKY_LAYOUT = "Y U I O P / H J K L ; / N M , . /"
MIDI_EXTS = (".mid", ".midi")
PIANO_PROGRAMS = set(range(0, 8))
VIOLIN_PROGRAMS = {40, 41}
STRING_PROGRAMS = {40, 41, 42, 43, 48, 49}


@dataclass(frozen=True)
class TrackSummary:
    track: int
    name: str
    programs: tuple[int, ...]
    notes: int
    pitch_min: int
    pitch_max: int
    median_pitch: float
    max_onset_poly: int
    monophonic_ratio: float


@dataclass(frozen=True)
class ValidationResult:
    events: int
    diagnostics: int
    unmapped: int
    duration_ms: int
    available: bool = True
    error: str = ""


def clean_label(text: str) -> str:
    return text.replace("\x00", "").strip()


def open_midi(path: Path) -> mido.MidiFile:
    try:
        return mido.MidiFile(path)
    except OSError as exc:
        if "data byte must be in range 0..127" not in str(exc):
            raise
        return mido.MidiFile(path, clip=True)


def read_track_metadata(path: Path) -> dict[int, dict[str, object]]:
    mid = open_midi(path)
    out: dict[int, dict[str, object]] = {}
    for idx, track in enumerate(mid.tracks):
        names: list[str] = []
        programs: set[int] = set()
        for msg in track:
            if msg.is_meta and msg.type in {"track_name", "instrument_name"}:
                name = clean_label(str(getattr(msg, "name", "")))
                if name:
                    names.append(name)
            elif not msg.is_meta and msg.type == "program_change":
                programs.add(int(msg.program))
        out[idx] = {
            "name": " / ".join(dict.fromkeys(names)),
            "programs": tuple(sorted(programs)),
        }
    return out


def build_track_summaries(parsed: dict, metadata: dict[int, dict[str, object]]) -> list[TrackSummary]:
    by_track: dict[int, list[dict]] = defaultdict(list)
    for note in parsed["notes"]:
        by_track[int(note["track"])].append(note)

    summaries: list[TrackSummary] = []
    for track_idx, notes in sorted(by_track.items()):
        starts: dict[int, int] = defaultdict(int)
        for note in notes:
            starts[int(note["start"])] += 1
        single = sum(1 for count in starts.values() if count == 1)
        meta = metadata.get(track_idx, {})
        name = clean_label(str(meta.get("name") or f"Track {track_idx}"))
        programs = tuple(int(p) for p in meta.get("programs", ()))
        pitches = [int(n["note"]) for n in notes]
        summaries.append(
            TrackSummary(
                track=track_idx,
                name=name,
                programs=programs,
                notes=len(notes),
                pitch_min=min(pitches),
                pitch_max=max(pitches),
                median_pitch=float(statistics.median(pitches)),
                max_onset_poly=max(starts.values()) if starts else 0,
                monophonic_ratio=(single / len(starts)) if starts else 0.0,
            )
        )
    return summaries


def parse_track_list(value: str, summaries: Iterable[TrackSummary]) -> set[int]:
    known = {s.track for s in summaries}
    tracks = {int(part.strip()) for part in value.split(",") if part.strip()}
    missing = sorted(tracks - known)
    if missing:
        raise SystemExit(f"Requested track(s) not found in MIDI notes: {missing}")
    return tracks


def violin_score(summary: TrackSummary) -> float:
    name = summary.name.lower()
    score = 0.0
    if "violin" in name or re.search(r"\bvl\b", name):
        score += 100.0
    if "melody" in name or "solo" in name:
        score += 20.0
    if "piano" in name:
        score -= 55.0
    if any(p in VIOLIN_PROGRAMS for p in summary.programs):
        score += 100.0
    elif any(p in STRING_PROGRAMS for p in summary.programs):
        score += 35.0
    if any(p in PIANO_PROGRAMS for p in summary.programs):
        score -= 35.0
    score += min(30.0, summary.notes / 18.0)
    score += summary.median_pitch * 0.45
    score += summary.monophonic_ratio * 22.0
    if summary.max_onset_poly <= 1:
        score += 12.0
    elif summary.max_onset_poly <= 2:
        score += 5.0
    return score


def piano_score(summary: TrackSummary) -> float:
    name = summary.name.lower()
    score = 0.0
    if "piano" in name:
        score += 100.0
    if any(p in PIANO_PROGRAMS for p in summary.programs):
        score += 100.0
    if "violin" in name:
        score -= 70.0
    if any(p in VIOLIN_PROGRAMS for p in summary.programs):
        score -= 70.0
    score += min(25.0, summary.notes / 20.0)
    if summary.max_onset_poly >= 2:
        score += 20.0
    if summary.median_pitch <= 68:
        score += 10.0
    return score


def choose_tracks(
    summaries: list[TrackSummary],
    violin_track_arg: str,
    piano_tracks_arg: str,
) -> tuple[int, set[int], bool]:
    if not summaries:
        raise SystemExit("No note tracks found in MIDI.")

    if violin_track_arg.lower() == "auto":
        violin = max(summaries, key=violin_score).track
    else:
        violin = parse_track_list(violin_track_arg, summaries).pop()

    if piano_tracks_arg.lower() == "auto":
        piano_candidates = [
            s.track
            for s in summaries
            if s.track != violin and piano_score(s) >= 30.0
        ]
        if not piano_candidates:
            piano_candidates = [s.track for s in summaries if s.track != violin]
        same_track_fallback = not piano_candidates
        return violin, set(piano_candidates), same_track_fallback

    piano_tracks = parse_track_list(piano_tracks_arg, summaries)
    return violin, piano_tracks, False


def default_downloads_dir() -> Path:
    return Path.home() / "Downloads"


def list_download_midis(downloads: Path, limit: int = 20) -> list[Path]:
    files: list[Path] = []
    for ext in MIDI_EXTS:
        files.extend(downloads.glob(f"*{ext}"))
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]


def resolve_midi_path(value: str | None, downloads: Path) -> Path:
    if value:
        raw = Path(value).expanduser()
        candidates = [raw]
        if not raw.is_absolute():
            candidates.append(downloads / raw)
        if raw.suffix.lower() not in MIDI_EXTS:
            candidates.extend((downloads / f"{value}{ext}") for ext in MIDI_EXTS)
        for path in candidates:
            if path.exists() and path.is_file():
                return path.resolve()
        raise SystemExit(f"MIDI not found. Tried path/name under Downloads: {value}")

    files = list_download_midis(downloads, limit=1)
    if not files:
        raise SystemExit(f"No .mid/.midi files found in {downloads}")
    return files[0].resolve()


def next_version_paths(out_dir: Path, midi_stem: str) -> tuple[Path, Path, Path, int]:
    safe_base = core.normalize_output_base(midi_stem)
    song_dir = out_dir / safe_base
    song_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(
        re.escape(safe_base)
        + r"_(?:domiso_script_sky_(?:violin|piano)|analysis_sky_violin_piano)_v(\d+)\.(?:txt|md)$",
        re.I,
    )
    max_version = 0
    for child in song_dir.iterdir():
        match = pattern.match(child.name)
        if match:
            max_version = max(max_version, int(match.group(1)))
    version = max_version + 1
    violin = song_dir / f"{safe_base}_domiso_script_sky_violin_v{version}.txt"
    piano = song_dir / f"{safe_base}_domiso_script_sky_piano_v{version}.txt"
    report = song_dir / f"{safe_base}_analysis_sky_violin_piano_v{version}.md"
    return violin, piano, report, version


def map_notes(parsed: dict, violin_track: int, profile_name: str) -> tuple[list[dict], dict[str, object]]:
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    profile = sky.PROFILES[profile_name]
    top_ids = core.build_top_ids(notes)
    base_shift = sky.choose_base_shift_profile(notes, top_ids, violin_track, tpb, profile)
    shifts, window_ticks, shift_changes = sky.choose_dynamic_shifts_profile(
        notes, top_ids, violin_track, tpb, base_shift, profile
    )
    tick_per_step = tpb / 4.0
    mapped: list[dict] = []
    for idx, note in enumerate(notes):
        window = min(len(shifts) - 1, max(0, int(note["start"]) // window_ticks))
        pitch, dist = sky.fold_and_snap_sky(int(note["note"]) + shifts[window])
        start_step = int(round(int(note["start"]) / tick_per_step))
        end_step = int(round(int(note["end"]) / tick_per_step))
        if end_step <= start_step:
            end_step = start_step + 1
        row = dict(note)
        row.update(
            {
                "src_idx": idx,
                "src_note": int(note["note"]),
                "pitch": pitch,
                "dist": dist,
                "start_step": start_step,
                "end_step": end_step,
                "dur_steps": end_step - start_step,
            }
        )
        mapped.append(row)

    return mapped, {
        "tempos": tempos,
        "tempo_steps": core.build_tempo_steps(tempos, tick_per_step),
        "profile": profile,
        "base_shift": base_shift,
        "shifts": shifts,
        "window_ticks": window_ticks,
        "shift_changes": shift_changes,
        "shift_summary": core.summarize_windows(shifts),
    }


def choose_violin_candidate(candidates: list[dict], prev_pitch: int | None) -> dict:
    scored: list[tuple[float, dict]] = []
    for note in candidates:
        score = note["vel"] / 96.0 + min(1.5, note["dur_steps"] * 0.25)
        pitch = int(note["pitch"])
        if 69 <= pitch <= 81:
            score += 1.0
        elif pitch < 67:
            score -= 0.6
        else:
            score += 0.2
        score += pitch * 0.02
        if prev_pitch is not None:
            leap = abs(pitch - prev_pitch)
            if leap <= 5:
                score += 0.8
            elif leap <= 9:
                score += 0.3
            elif leap >= 14:
                score -= 0.8
        scored.append((score, note))
    scored.sort(key=lambda item: (item[0], item[1]["pitch"], item[1]["dur_steps"]), reverse=True)
    return scored[0][1]


def build_violin_intervals(
    mapped: list[dict],
    violin_track: int,
    legato: str,
) -> tuple[list[tuple[int, int, int]], set[int], dict[str, int]]:
    by_step: dict[int, list[dict]] = defaultdict(list)
    for note in mapped:
        if int(note["track"]) == violin_track:
            by_step[int(note["start_step"])].append(note)

    selected: list[dict] = []
    prev_pitch: int | None = None
    same_time_dropped = 0
    for step in sorted(by_step):
        candidates = by_step[step]
        chosen = choose_violin_candidate(candidates, prev_pitch)
        selected.append(chosen)
        prev_pitch = int(chosen["pitch"])
        same_time_dropped += max(0, len(candidates) - 1)

    phrase_span_limit = {"off": 0, "light": 16, "long": 24}[legato]
    gap_limit = {"off": -1, "light": 10, "long": 16}[legato]
    intervals: list[tuple[int, int, int]] = []
    source_ids: set[int] = set()
    extended = 0
    same_key_release_cuts = 0
    grid_limited_repeats = 0

    for idx, note in enumerate(selected):
        start = int(note["start_step"])
        end = int(note["end_step"])
        pitch = int(note["pitch"])
        source_ids.add(int(note["src_idx"]))
        if idx + 1 < len(selected):
            nxt = selected[idx + 1]
            next_start = int(nxt["start_step"])
            next_pitch = int(nxt["pitch"])
            phrase_neighbor = (
                legato != "off"
                and (next_start - start) <= phrase_span_limit
                and (next_start - end) <= gap_limit
            )
            if phrase_neighbor and next_start > start:
                target = next_start if next_pitch != pitch else next_start - 1
                if target > end:
                    end = target
                    extended += 1
            if next_pitch == pitch and end >= next_start:
                if next_start - start >= 2:
                    end = next_start - 1
                    same_key_release_cuts += 1
                else:
                    grid_limited_repeats += 1
        intervals.append((start, max(start + 1, end), pitch))

    return intervals, source_ids, {
        "violin_source_notes": sum(1 for n in mapped if int(n["track"]) == violin_track),
        "violin_selected_notes": len(selected),
        "violin_same_time_dropped": same_time_dropped,
        "violin_output_intervals": len(intervals),
        "violin_legato_extended_notes": extended,
        "violin_same_key_release_cuts": same_key_release_cuts,
        "violin_grid_limited_same_key_repeats": grid_limited_repeats,
    }


def piano_step_cap(step: int, max_poly: int, has_long_remaining: bool) -> int:
    if step % 16 == 0:
        return max_poly
    if step % 4 == 0:
        return min(max_poly, 3)
    if step % 2 == 0:
        return min(max_poly, 2)
    return 1 if has_long_remaining else 0


def build_piano_intervals(
    mapped: list[dict],
    piano_tracks: set[int],
    violin_source_ids: set[int],
    same_track_fallback: bool,
    max_poly: int,
) -> tuple[list[tuple[int, int, int]], dict[str, int]]:
    by_step: dict[int, list[dict]] = defaultdict(list)
    for note in mapped:
        track = int(note["track"])
        if piano_tracks:
            include = track in piano_tracks
        else:
            include = same_track_fallback and int(note["src_idx"]) not in violin_source_ids
        if include:
            by_step[int(note["start_step"])].append(note)

    intervals: list[tuple[int, int, int]] = []
    kept_total = 0
    dropped_total = 0
    dedup_dropped = 0

    for step in sorted(by_step):
        arr = by_step[step]
        dedup: dict[int, tuple[float, dict]] = {}
        for note in arr:
            score = note["dur_steps"] * 0.5 + note["vel"] / 127.0
            if int(note["track"]) in piano_tracks:
                score += 0.2
            if note["pitch"] not in dedup or score > dedup[note["pitch"]][0]:
                dedup[note["pitch"]] = (score, note)
        vals = [item[1] for item in dedup.values()]
        dedup_dropped += len(arr) - len(vals)

        keep: list[dict] = []
        basses = sorted(
            [n for n in vals if int(n["pitch"]) <= 67 or int(n["track"]) in piano_tracks],
            key=lambda n: (int(n["pitch"]), -int(n["dur_steps"]), -int(n["vel"])),
        )
        if basses and (step % 4 == 0 or (step % 2 == 0 and any(n["dur_steps"] >= 2 for n in basses))):
            keep.append(basses[0])

        remaining = [n for n in vals if n not in keep]
        cap = piano_step_cap(step, max_poly, any(n["dur_steps"] >= 4 for n in remaining))
        scored: list[tuple[float, dict]] = []
        for note in remaining:
            pitch = int(note["pitch"])
            score = 0.0
            if int(note["track"]) in piano_tracks:
                score += 0.8
            if pitch >= 69:
                score += 0.7
            if pitch <= 64:
                score -= 0.35
            score += min(1.0, int(note["dur_steps"]) / 6.0)
            score += int(note["vel"]) / 160.0
            if step % 4 == 0:
                score += 0.25
            scored.append((score, note))
        scored.sort(key=lambda item: (-item[0], -int(item[1]["pitch"]), -int(item[1]["dur_steps"])))

        for _, note in scored:
            if len(keep) >= cap:
                break
            keep.append(note)

        for note in keep:
            start = int(note["start_step"])
            intervals.append((start, max(start + 1, int(note["end_step"])), int(note["pitch"])))
        kept_total += len(keep)
        dropped_total += max(0, len(vals) - len(keep))

    merged = base.merge_intervals_strict(intervals)
    return merged, {
        "piano_source_notes": sum(
            1
            for n in mapped
            if (int(n["track"]) in piano_tracks)
            or (same_track_fallback and int(n["src_idx"]) not in violin_source_ids)
        ),
        "piano_candidates_kept_before_merge": kept_total,
        "piano_candidates_dropped_before_merge": dropped_total,
        "piano_dedup_dropped": dedup_dropped,
        "piano_output_intervals": len(merged),
    }


def build_step_ms(total_steps: int, tempo_steps: list[tuple[int, int]]) -> list[float]:
    return sky.build_step_ms(total_steps + 2, tempo_steps)


def stability(intervals: list[tuple[int, int, int]], step_ms: list[float]) -> dict[str, float]:
    onset_steps = sorted({s for s, _, _ in intervals})
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
    gaps = [step_ms[onset_steps[i]] - step_ms[onset_steps[i - 1]] for i in range(1, len(onset_steps))]
    per_pitch: dict[int, list[int]] = defaultdict(list)
    for start, _, pitch in intervals:
        per_pitch[pitch].append(start)
    same_key_gaps: list[float] = []
    for starts in per_pitch.values():
        starts.sort()
        same_key_gaps.extend(step_ms[starts[i]] - step_ms[starts[i - 1]] for i in range(1, len(starts)))
    return {
        "clusters_per_sec_peak": float(peak),
        "min_cluster_gap_ms": round(min(gaps), 1) if gaps else 0.0,
        "same_key_min_gap_ms": round(min(same_key_gaps), 1) if same_key_gaps else 0.0,
    }


def safe_header(lines: list[str]) -> list[str]:
    note_token = re.compile(r"^(?:[+\-]*[0-7][/\-.]*|[+\-]*[1-7][#b][/\-.]*)$")
    for line in lines:
        for token in line.split():
            if note_token.match(token):
                raise RuntimeError(f"Unsafe metadata token for Domiso parser: {token!r}")
    return lines


def render_text(
    *,
    title: str,
    source: str,
    kind: str,
    track_info: str,
    shift_summary: str,
    duration_s: float,
    initial_bpm: int,
    tempo_steps: list[tuple[int, int]],
    intervals: list[tuple[int, int, int]],
    total_steps: int,
    max_poly: int,
) -> str:
    segments = base.intervals_to_segments_limited(intervals, total_steps, max_poly)
    lines = core.serialize_voice(segments, tempo_steps)
    header = safe_header(
        [
            f"Title:{title}",
            f"Source:{source}",
            f"Info:kind={kind};{track_info};layout=Sky15;range=C4-C6",
            f"Info:transpose={shift_summary.replace(' ', '')}",
            f"Info:duration~{duration_s:.1f}s;grid=sixteenth;countin=none",
            "",
            f"bpm={initial_bpm}",
            "",
            f";Sky{kind}",
        ]
    )
    text = "\n".join(header + lines).rstrip() + "\n"
    accidental = re.compile(r"(?<![A-Za-z0-9_])[+\-]*[1-7][#b](?![A-Za-z0-9_])")
    if accidental.search(text):
        raise RuntimeError(f"{kind} output contains accidental Domiso tokens")
    return text


def validate_text(text: str) -> ValidationResult:
    if str(ORCHESTRA_DIR) not in sys.path:
        sys.path.insert(0, str(ORCHESTRA_DIR))
    try:
        from domiso_orchestra.domiso_parser import parse_domiso_text
        from domiso_orchestra.keymaps import map_midi_to_key
    except Exception as exc:
        return ValidationResult(0, 0, 0, 0, available=False, error=str(exc))

    events, diagnostics, total_ms = parse_domiso_text(text, pitch_naming="standard")
    unmapped = sum(1 for event in events if map_midi_to_key(event.midi_note, "sky15") is None)
    return ValidationResult(len(events), len(diagnostics), unmapped, total_ms)


def write_report(
    path: Path,
    *,
    input_path: Path,
    summaries: list[TrackSummary],
    violin_track: int,
    piano_tracks: set[int],
    same_track_fallback: bool,
    profile_name: str,
    mapping_info: dict[str, object],
    duration_s: float,
    version: int,
    violin_path: Path,
    piano_path: Path,
    violin_stats: dict[str, int],
    piano_stats: dict[str, int],
    violin_validation: ValidationResult,
    piano_validation: ValidationResult,
    violin_stability: dict[str, float],
    piano_stability: dict[str, float],
) -> None:
    track_lines = []
    for s in summaries:
        programs = ",".join(str(p) for p in s.programs) if s.programs else "none"
        track_lines.append(
            f"- Track {s.track}: name={s.name}, programs={programs}, notes={s.notes}, "
            f"pitch_range={s.pitch_min}..{s.pitch_max}, median={s.median_pitch:.1f}, "
            f"max_onset_poly={s.max_onset_poly}"
        )
    piano_text = ",".join(str(t) for t in sorted(piano_tracks)) if piano_tracks else "same-track-fallback"
    lines = [
        f"# Analysis (Auto Sky Violin + Piano): {input_path.name}",
        "",
        "## Source Tracks",
        *track_lines,
        "",
        "## Arrangement Decisions",
        f"- selected_violin_track: {violin_track}",
        f"- selected_piano_tracks: {piano_text}",
        f"- same_track_fallback: {same_track_fallback}",
        "- violin keeps one melodic note per onset and uses light phrase legato",
        "- piano keeps bass anchors plus selected upper harmony, capped for Sky15 playability",
        "- both txt files share tempo map and transpose windows for Domiso-Orchestra sync",
        "",
        "## Mapping",
        f"- profile: {profile_name}",
        f"- version: {version}",
        f"- base_shift: {mapping_info['base_shift']}",
        f"- dynamic_windows: {mapping_info['shift_summary']}",
        f"- shift_changes: {mapping_info['shift_changes']}",
        f"- tempo_events: {len(mapping_info['tempo_steps'])}",
        f"- duration_s: {duration_s:.2f}",
        "",
        "## Output Files",
        f"- violin: {violin_path}",
        f"- piano: {piano_path}",
        "",
        "## Counts",
        *[f"- {key}: {value}" for key, value in violin_stats.items()],
        *[f"- {key}: {value}" for key, value in piano_stats.items()],
        "",
        "## Validation",
        (
            "- violin: "
            f"events={violin_validation.events}, diagnostics={violin_validation.diagnostics}, "
            f"unmapped={violin_validation.unmapped}, duration_ms={violin_validation.duration_ms}"
        ),
        (
            "- piano: "
            f"events={piano_validation.events}, diagnostics={piano_validation.diagnostics}, "
            f"unmapped={piano_validation.unmapped}, duration_ms={piano_validation.duration_ms}"
        ),
        "",
        "## Input Stability",
        f"- violin: {violin_stability}",
        f"- piano: {piano_stability}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def convert(args: argparse.Namespace) -> dict[str, object]:
    downloads = Path(args.downloads).expanduser()
    input_path = resolve_midi_path(args.midi, downloads)
    parsed = core.parse_midi(str(input_path))
    metadata = read_track_metadata(input_path)
    summaries = build_track_summaries(parsed, metadata)
    violin_track, piano_tracks, same_track_fallback = choose_tracks(
        summaries, args.violin_track, args.piano_tracks
    )

    metrics = sky.analyze_midi(parsed)
    if args.profile == "auto":
        profile_name, _ = sky.recommend_profile(metrics)
    else:
        profile_name = args.profile

    mapped, mapping_info = map_notes(parsed, violin_track, profile_name)
    total_steps = max(note["end_step"] for note in mapped) + 1
    step_ms = build_step_ms(total_steps, mapping_info["tempo_steps"])
    duration_s = core.tick_to_seconds(parsed["max_tick"], mapping_info["tempos"], parsed["tpb"])

    violin_intervals, violin_ids, violin_stats = build_violin_intervals(
        mapped, violin_track, args.violin_legato
    )
    piano_intervals, piano_stats = build_piano_intervals(
        mapped,
        piano_tracks,
        violin_ids,
        same_track_fallback,
        max(1, min(8, int(args.piano_max_poly))),
    )

    out_dir = Path(args.out_dir).expanduser()
    violin_path, piano_path, report_path, version = next_version_paths(out_dir, input_path.stem)
    safe_title = core.normalize_output_base(input_path.stem).replace(" ", "-")
    violin_text = render_text(
        title=f"{safe_title}-Sky-Duet",
        source=input_path.name,
        kind="Violin",
        track_info=f"trackV={violin_track};trackP={','.join(str(t) for t in sorted(piano_tracks)) or 'fallback'}",
        shift_summary=str(mapping_info["shift_summary"]),
        duration_s=duration_s,
        initial_bpm=int(mapping_info["tempos"][0][1]),
        tempo_steps=mapping_info["tempo_steps"],
        intervals=violin_intervals,
        total_steps=total_steps,
        max_poly=1,
    )
    piano_text = render_text(
        title=f"{safe_title}-Sky-Duet",
        source=input_path.name,
        kind="Piano",
        track_info=f"trackV={violin_track};trackP={','.join(str(t) for t in sorted(piano_tracks)) or 'fallback'}",
        shift_summary=str(mapping_info["shift_summary"]),
        duration_s=duration_s,
        initial_bpm=int(mapping_info["tempos"][0][1]),
        tempo_steps=mapping_info["tempo_steps"],
        intervals=piano_intervals,
        total_steps=total_steps,
        max_poly=max(1, min(8, int(args.piano_max_poly))),
    )

    violin_validation = validate_text(violin_text)
    piano_validation = validate_text(piano_text)
    if violin_validation.available and (
        violin_validation.diagnostics or violin_validation.unmapped or piano_validation.diagnostics or piano_validation.unmapped
    ):
        raise RuntimeError(
            "Validation failed: "
            f"violin diagnostics={violin_validation.diagnostics} unmapped={violin_validation.unmapped}; "
            f"piano diagnostics={piano_validation.diagnostics} unmapped={piano_validation.unmapped}"
        )

    violin_path.write_text(violin_text, encoding="utf-8", newline="\n")
    piano_path.write_text(piano_text, encoding="utf-8", newline="\n")
    write_report(
        report_path,
        input_path=input_path,
        summaries=summaries,
        violin_track=violin_track,
        piano_tracks=piano_tracks,
        same_track_fallback=same_track_fallback,
        profile_name=profile_name,
        mapping_info=mapping_info,
        duration_s=duration_s,
        version=version,
        violin_path=violin_path,
        piano_path=piano_path,
        violin_stats=violin_stats,
        piano_stats=piano_stats,
        violin_validation=violin_validation,
        piano_validation=piano_validation,
        violin_stability=stability(violin_intervals, step_ms),
        piano_stability=stability(piano_intervals, step_ms),
    )

    return {
        "input": input_path,
        "violin": violin_path,
        "piano": piano_path,
        "report": report_path,
        "version": version,
        "profile": profile_name,
        "violin_track": violin_track,
        "piano_tracks": sorted(piano_tracks),
        "same_track_fallback": same_track_fallback,
        "shift_summary": mapping_info["shift_summary"],
        "violin_validation": violin_validation,
        "piano_validation": piano_validation,
    }


def print_track_analysis(summaries: list[TrackSummary], violin_track: int, piano_tracks: set[int]) -> None:
    for summary in summaries:
        programs = ",".join(str(p) for p in summary.programs) if summary.programs else "none"
        marker = []
        if summary.track == violin_track:
            marker.append("VIOLIN")
        if summary.track in piano_tracks:
            marker.append("PIANO")
        tag = f" [{' '.join(marker)}]" if marker else ""
        print(
            f"track={summary.track}{tag} name={summary.name!r} programs={programs} "
            f"notes={summary.notes} range={summary.pitch_min}..{summary.pitch_max} "
            f"median={summary.median_pitch:.1f} max_poly={summary.max_onset_poly}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Auto split a Downloads MIDI into Sky15 violin+piano Domiso txt files."
    )
    parser.add_argument(
        "midi",
        nargs="?",
        help="Optional MIDI path or filename. If omitted, newest .mid/.midi in Downloads is used.",
    )
    parser.add_argument("--downloads", default=str(default_downloads_dir()))
    parser.add_argument("--out-dir", default=str(ROOT_DIR / "txt"))
    parser.add_argument("--profile", default="auto", choices=["auto"] + sorted(sky.PROFILES))
    parser.add_argument("--violin-track", default="auto")
    parser.add_argument("--piano-tracks", default="auto")
    parser.add_argument("--violin-legato", default="light", choices=["off", "light", "long"])
    parser.add_argument("--piano-max-poly", default=4, type=int)
    parser.add_argument("--list", action="store_true", help="List recent MIDI files in Downloads and exit.")
    parser.add_argument("--analyze-only", action="store_true", help="Print selected tracks without writing txt files.")
    args = parser.parse_args()

    downloads = Path(args.downloads).expanduser()
    if args.list:
        for path in list_download_midis(downloads):
            print(path)
        return

    input_path = resolve_midi_path(args.midi, downloads)
    parsed = core.parse_midi(str(input_path))
    summaries = build_track_summaries(parsed, read_track_metadata(input_path))
    violin_track, piano_tracks, same_track_fallback = choose_tracks(
        summaries, args.violin_track, args.piano_tracks
    )

    if args.analyze_only:
        print(f"input={input_path}")
        print_track_analysis(summaries, violin_track, piano_tracks)
        print(f"same_track_fallback={same_track_fallback}")
        return

    result = convert(args)
    vv: ValidationResult = result["violin_validation"]  # type: ignore[assignment]
    pv: ValidationResult = result["piano_validation"]  # type: ignore[assignment]
    print(f"input={result['input']}")
    print(f"profile={result['profile']}")
    print(f"tracks=violin:{result['violin_track']} piano:{','.join(str(t) for t in result['piano_tracks']) or 'fallback'}")
    print(f"transpose={result['shift_summary']}")
    print(f"violin={result['violin']}")
    print(f"piano={result['piano']}")
    print(f"analysis_report={result['report']}")
    if vv.available and pv.available:
        print(f"validation_violin=events:{vv.events} diagnostics:{vv.diagnostics} unmapped:{vv.unmapped}")
        print(f"validation_piano=events:{pv.events} diagnostics:{pv.diagnostics} unmapped:{pv.unmapped}")
    else:
        print(f"validation_skipped={vv.error or pv.error}")


if __name__ == "__main__":
    main()
