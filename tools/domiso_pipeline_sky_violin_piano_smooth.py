#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import domiso_pipeline_literal as base
import domiso_pipeline_sky_violin_piano as normal
import domiso_pipeline_sky_melodylock as sky
import midi_to_domiso_dense3layer as core


@dataclass(frozen=True)
class SmoothPreset:
    min_onset_ms: int
    phrase_gap_ms: int
    same_pitch_merge_ms: int
    max_legato_span_ms: int


PRESETS = {
    "light": SmoothPreset(
        min_onset_ms=160,
        phrase_gap_ms=520,
        same_pitch_merge_ms=650,
        max_legato_span_ms=1400,
    ),
    "balanced": SmoothPreset(
        min_onset_ms=190,
        phrase_gap_ms=680,
        same_pitch_merge_ms=850,
        max_legato_span_ms=1800,
    ),
    "strong": SmoothPreset(
        min_onset_ms=230,
        phrase_gap_ms=850,
        same_pitch_merge_ms=1100,
        max_legato_span_ms=2300,
    ),
}


def next_smooth_version_paths(out_dir: Path, midi_stem: str) -> tuple[Path, Path, Path, int]:
    safe_base = core.normalize_output_base(midi_stem)
    song_dir = out_dir / safe_base
    song_dir.mkdir(parents=True, exist_ok=True)
    max_version = 0
    for child in song_dir.iterdir():
        name = child.name.lower()
        prefix = f"{safe_base.lower()}_"
        if not name.startswith(prefix):
            continue
        if "_domiso_script_sky_smooth_violin_v" in name or "_domiso_script_sky_smooth_piano_v" in name:
            stem = name.rsplit("_v", 1)[-1].split(".", 1)[0]
        elif "_analysis_sky_smooth_violin_piano_v" in name:
            stem = name.rsplit("_v", 1)[-1].split(".", 1)[0]
        else:
            continue
        if stem.isdigit():
            max_version = max(max_version, int(stem))
    version = max_version + 1
    violin = song_dir / f"{safe_base}_domiso_script_sky_smooth_violin_v{version}.txt"
    piano = song_dir / f"{safe_base}_domiso_script_sky_smooth_piano_v{version}.txt"
    report = song_dir / f"{safe_base}_analysis_sky_smooth_violin_piano_v{version}.md"
    return violin, piano, report, version


def step_to_ms(step_ms: list[float], step: int) -> float:
    if not step_ms:
        return 0.0
    idx = min(max(0, step), len(step_ms) - 1)
    return step_ms[idx]


def duration_ms(step_ms: list[float], start: int, end: int) -> float:
    return max(0.0, step_to_ms(step_ms, end) - step_to_ms(step_ms, start))


def choose_one_violin_note(notes: list[dict], prev_pitch: int | None) -> dict:
    return normal.choose_violin_candidate(notes, prev_pitch)


def is_strong_step(step: int) -> bool:
    return step % 4 == 0


def build_smooth_violin_intervals(
    mapped: list[dict],
    violin_track: int,
    step_ms: list[float],
    preset: SmoothPreset,
) -> tuple[list[tuple[int, int, int]], set[int], dict[str, int]]:
    by_step: dict[int, list[dict]] = defaultdict(list)
    all_violin_ids: set[int] = set()
    for note in mapped:
        if int(note["track"]) != violin_track:
            continue
        by_step[int(note["start_step"])].append(note)
        all_violin_ids.add(int(note["src_idx"]))

    selected: list[dict] = []
    same_time_dropped = 0
    prev_pitch: int | None = None
    for step in sorted(by_step):
        chosen = dict(choose_one_violin_note(by_step[step], prev_pitch))
        chosen["absorbed_ids"] = {int(n["src_idx"]) for n in by_step[step]}
        selected.append(chosen)
        prev_pitch = int(chosen["pitch"])
        same_time_dropped += max(0, len(by_step[step]) - 1)

    kept: list[dict] = []
    rate_dropped = 0
    same_pitch_merged = 0
    beat_replacements = 0
    absorbed_into_previous = 0

    for note in selected:
        note = dict(note)
        note.setdefault("absorbed_ids", {int(note["src_idx"])})
        if not kept:
            kept.append(note)
            continue

        prev = kept[-1]
        gap_ms = step_to_ms(step_ms, int(note["start_step"])) - step_to_ms(step_ms, int(prev["start_step"]))
        same_pitch = int(note["pitch"]) == int(prev["pitch"])

        if same_pitch and gap_ms <= preset.same_pitch_merge_ms:
            prev["end_step"] = max(int(prev["end_step"]), int(note["end_step"]))
            prev["absorbed_ids"] = set(prev.get("absorbed_ids", set())) | set(note.get("absorbed_ids", set()))
            same_pitch_merged += 1
            continue

        if gap_ms < preset.min_onset_ms:
            prev_is_strong = is_strong_step(int(prev["start_step"]))
            note_is_strong = is_strong_step(int(note["start_step"]))
            if note_is_strong and not prev_is_strong:
                note["absorbed_ids"] = set(note.get("absorbed_ids", set())) | set(prev.get("absorbed_ids", set()))
                kept[-1] = note
                beat_replacements += 1
            else:
                prev["end_step"] = max(int(prev["end_step"]), int(note["end_step"]))
                prev["absorbed_ids"] = set(prev.get("absorbed_ids", set())) | set(note.get("absorbed_ids", set()))
                rate_dropped += 1
                absorbed_into_previous += 1
            continue

        kept.append(note)

    intervals: list[tuple[int, int, int]] = []
    legato_extended = 0
    min_duration_extended = 0
    source_ids: set[int] = set()

    for idx, note in enumerate(kept):
        source_ids.update(int(i) for i in note.get("absorbed_ids", {int(note["src_idx"])}))
        start = int(note["start_step"])
        end = max(start + 1, int(note["end_step"]))
        pitch = int(note["pitch"])

        if idx + 1 < len(kept):
            nxt = kept[idx + 1]
            next_start = int(nxt["start_step"])
            gap_to_next_ms = step_to_ms(step_ms, next_start) - step_to_ms(step_ms, end)
            span_ms = step_to_ms(step_ms, next_start) - step_to_ms(step_ms, start)
            if (
                next_start > start
                and gap_to_next_ms <= preset.phrase_gap_ms
                and span_ms <= preset.max_legato_span_ms
            ):
                if next_start > end:
                    end = next_start
                    legato_extended += 1
                elif end > next_start:
                    end = next_start

        current_ms = duration_ms(step_ms, start, end)
        target_min = min(preset.min_onset_ms, 260)
        if current_ms < target_min:
            needed_steps = max(1, int(math.ceil(target_min / max(1.0, duration_ms(step_ms, start, start + 1)))))
            proposed_end = start + needed_steps
            if idx + 1 < len(kept):
                proposed_end = min(proposed_end, int(kept[idx + 1]["start_step"]))
            if proposed_end > end:
                end = proposed_end
                min_duration_extended += 1

        if end > start:
            intervals.append((start, end, pitch))

    merged = base.merge_intervals_strict(intervals)
    return merged, source_ids | all_violin_ids, {
        "violin_source_notes": sum(1 for n in mapped if int(n["track"]) == violin_track),
        "violin_selected_onsets": len(selected),
        "violin_smooth_kept_onsets": len(kept),
        "violin_same_time_dropped": same_time_dropped,
        "violin_rate_dropped": rate_dropped,
        "violin_same_pitch_merged": same_pitch_merged,
        "violin_beat_replacements": beat_replacements,
        "violin_absorbed_into_previous": absorbed_into_previous,
        "violin_legato_extended_notes": legato_extended,
        "violin_min_duration_extended": min_duration_extended,
        "violin_output_intervals": len(merged),
    }


def text_metrics(text: str) -> dict[str, float]:
    if str(normal.ORCHESTRA_DIR) not in sys.path:
        sys.path.insert(0, str(normal.ORCHESTRA_DIR))
    from domiso_orchestra.domiso_parser import parse_domiso_text

    events, diagnostics, total_ms = parse_domiso_text(text, pitch_naming="standard")
    if not events:
        return {
            "events": 0,
            "diagnostics": float(len(diagnostics)),
            "duration_s": round(total_ms / 1000, 1),
            "short250_pct": 0.0,
            "actual_press150_pct": 0.0,
            "median_duration_ms": 0.0,
            "min_onset_gap_ms": 0.0,
        }
    durs = [e.duration_ms for e in events]
    starts = sorted(e.time_ms for e in events)
    gaps = [starts[i] - starts[i - 1] for i in range(1, len(starts))]
    track = note_events_to_track_for_metrics(text)
    press = normal_press_durations(track)
    return {
        "events": float(len(events)),
        "diagnostics": float(len(diagnostics)),
        "duration_s": round(total_ms / 1000, 1),
        "short250_pct": round(sum(d <= 250 for d in durs) / len(durs) * 100, 1),
        "actual_press150_pct": round(sum(p <= 150 for p in press) / len(press) * 100, 1) if press else 0.0,
        "median_duration_ms": round(statistics.median(durs), 1),
        "min_onset_gap_ms": round(min(gaps), 1) if gaps else 0.0,
    }


def normal_press_durations(track: dict) -> list[int]:
    if str(normal.ORCHESTRA_DIR) not in sys.path:
        sys.path.insert(0, str(normal.ORCHESTRA_DIR))
    from domiso_orchestra.playback import PlaybackProfile, build_actions

    actions = build_actions([track], PlaybackProfile().to_dict())
    stacks: dict[str, list[int]] = {}
    out: list[int] = []
    for action in actions:
        if action.down:
            stacks.setdefault(action.key, []).append(action.time_ms)
        elif stacks.get(action.key):
            out.append(action.time_ms - stacks[action.key].pop(0))
    return out


def note_events_to_track_for_metrics(text: str) -> dict:
    if str(normal.ORCHESTRA_DIR) not in sys.path:
        sys.path.insert(0, str(normal.ORCHESTRA_DIR))
    from domiso_orchestra.domiso_parser import note_events_to_track

    return note_events_to_track(
        track_id="metric",
        name="metric",
        text=text,
        layout="sky15",
        pitch_naming="standard",
    )

def write_smooth_report(
    path: Path,
    *,
    input_path: Path,
    version: int,
    style: str,
    preset: SmoothPreset,
    summaries: list[normal.TrackSummary],
    violin_track: int,
    piano_tracks: set[int],
    same_track_fallback: bool,
    mapping_info: dict[str, object],
    duration_s: float,
    violin_path: Path,
    piano_path: Path,
    violin_stats: dict[str, int],
    piano_stats: dict[str, int],
    violin_validation: normal.ValidationResult,
    piano_validation: normal.ValidationResult,
    violin_metrics: dict[str, float],
) -> None:
    track_lines = []
    for summary in summaries:
        programs = ",".join(str(p) for p in summary.programs) if summary.programs else "none"
        track_lines.append(
            f"- Track {summary.track}: name={summary.name}, programs={programs}, "
            f"notes={summary.notes}, pitch_range={summary.pitch_min}..{summary.pitch_max}, "
            f"median={summary.median_pitch:.1f}, max_onset_poly={summary.max_onset_poly}"
        )

    piano_text = ",".join(str(t) for t in sorted(piano_tracks)) if piano_tracks else "same-track-fallback"
    lines = [
        f"# Analysis (Smooth Sky Violin + Piano): {input_path.name}",
        "",
        "## Source Tracks",
        *track_lines,
        "",
        "## Smooth Violin Settings",
        f"- style: {style}",
        f"- min_onset_ms: {preset.min_onset_ms}",
        f"- phrase_gap_ms: {preset.phrase_gap_ms}",
        f"- same_pitch_merge_ms: {preset.same_pitch_merge_ms}",
        f"- max_legato_span_ms: {preset.max_legato_span_ms}",
        "",
        "## Arrangement Decisions",
        f"- selected_violin_track: {violin_track}",
        f"- selected_piano_tracks: {piano_text}",
        f"- same_track_fallback: {same_track_fallback}",
        "- violin smooth mode limits rapid re-attacks, merges close same-pitch notes, and extends phrase-internal note tails",
        "- piano uses the normal accompaniment selector so only the violin feel changes substantially",
        "- both txt files share tempo map and transpose windows for Domiso-Orchestra sync",
        "",
        "## Mapping",
        f"- profile: {mapping_info['profile'].name}",
        f"- version: {version}",
        f"- base_shift: {mapping_info['base_shift']}",
        f"- dynamic_windows: {mapping_info['shift_summary']}",
        f"- shift_changes: {mapping_info['shift_changes']}",
        f"- tempo_events: {len(mapping_info['tempo_steps'])}",
        f"- duration_s: {duration_s:.2f}",
        "",
        "## Output Files",
        f"- smooth_violin: {violin_path}",
        f"- smooth_piano: {piano_path}",
        "",
        "## Counts",
        *[f"- {key}: {value}" for key, value in violin_stats.items()],
        *[f"- {key}: {value}" for key, value in piano_stats.items()],
        "",
        "## Violin Feel Metrics",
        *[f"- {key}: {value}" for key, value in violin_metrics.items()],
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
    ]
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def convert(args: argparse.Namespace) -> dict[str, object]:
    downloads = Path(args.downloads).expanduser()
    input_path = normal.resolve_midi_path(args.midi, downloads)
    parsed = core.parse_midi(str(input_path))
    summaries = normal.build_track_summaries(parsed, normal.read_track_metadata(input_path))
    violin_track, piano_tracks, same_track_fallback = normal.choose_tracks(
        summaries, args.violin_track, args.piano_tracks
    )

    metrics = sky.analyze_midi(parsed)
    profile_name = sky.recommend_profile(metrics)[0] if args.profile == "auto" else args.profile
    mapped, mapping_info = normal.map_notes(parsed, violin_track, profile_name)
    total_steps = max(note["end_step"] for note in mapped) + 1
    step_ms = normal.build_step_ms(total_steps, mapping_info["tempo_steps"])
    duration_s = core.tick_to_seconds(parsed["max_tick"], mapping_info["tempos"], parsed["tpb"])

    preset = PRESETS[args.violin_style]
    if args.min_onset_ms is not None:
        preset = SmoothPreset(
            min_onset_ms=int(args.min_onset_ms),
            phrase_gap_ms=preset.phrase_gap_ms,
            same_pitch_merge_ms=preset.same_pitch_merge_ms,
            max_legato_span_ms=preset.max_legato_span_ms,
        )

    violin_intervals, violin_ids, violin_stats = build_smooth_violin_intervals(
        mapped,
        violin_track,
        step_ms,
        preset,
    )
    piano_intervals, piano_stats = normal.build_piano_intervals(
        mapped,
        piano_tracks,
        violin_ids,
        same_track_fallback,
        max(1, min(8, int(args.piano_max_poly))),
    )

    out_dir = Path(args.out_dir).expanduser()
    violin_path, piano_path, report_path, version = next_smooth_version_paths(out_dir, input_path.stem)
    safe_title = core.normalize_output_base(input_path.stem).replace(" ", "-")
    track_info = f"trackV={violin_track};trackP={','.join(str(t) for t in sorted(piano_tracks)) or 'fallback'}"

    violin_text = normal.render_text(
        title=f"{safe_title}-Sky-Smooth-Duet",
        source=input_path.name,
        kind="SmoothViolin",
        track_info=track_info,
        shift_summary=str(mapping_info["shift_summary"]),
        duration_s=duration_s,
        initial_bpm=int(mapping_info["tempos"][0][1]),
        tempo_steps=mapping_info["tempo_steps"],
        intervals=violin_intervals,
        total_steps=total_steps,
        max_poly=1,
    )
    piano_text = normal.render_text(
        title=f"{safe_title}-Sky-Smooth-Duet",
        source=input_path.name,
        kind="SmoothPiano",
        track_info=track_info,
        shift_summary=str(mapping_info["shift_summary"]),
        duration_s=duration_s,
        initial_bpm=int(mapping_info["tempos"][0][1]),
        tempo_steps=mapping_info["tempo_steps"],
        intervals=piano_intervals,
        total_steps=total_steps,
        max_poly=max(1, min(8, int(args.piano_max_poly))),
    )

    violin_validation = normal.validate_text(violin_text)
    piano_validation = normal.validate_text(piano_text)
    if violin_validation.available and (
        violin_validation.diagnostics
        or violin_validation.unmapped
        or piano_validation.diagnostics
        or piano_validation.unmapped
    ):
        raise RuntimeError(
            "Validation failed: "
            f"violin diagnostics={violin_validation.diagnostics} unmapped={violin_validation.unmapped}; "
            f"piano diagnostics={piano_validation.diagnostics} unmapped={piano_validation.unmapped}"
        )

    violin_path.write_text(violin_text, encoding="utf-8", newline="\n")
    piano_path.write_text(piano_text, encoding="utf-8", newline="\n")
    violin_metrics = text_metrics(violin_text)
    write_smooth_report(
        report_path,
        input_path=input_path,
        version=version,
        style=args.violin_style,
        preset=preset,
        summaries=summaries,
        violin_track=violin_track,
        piano_tracks=piano_tracks,
        same_track_fallback=same_track_fallback,
        mapping_info=mapping_info,
        duration_s=duration_s,
        violin_path=violin_path,
        piano_path=piano_path,
        violin_stats=violin_stats,
        piano_stats=piano_stats,
        violin_validation=violin_validation,
        piano_validation=piano_validation,
        violin_metrics=violin_metrics,
    )

    return {
        "input": input_path,
        "profile": profile_name,
        "style": args.violin_style,
        "violin_track": violin_track,
        "piano_tracks": sorted(piano_tracks),
        "same_track_fallback": same_track_fallback,
        "transpose": mapping_info["shift_summary"],
        "violin": violin_path,
        "piano": piano_path,
        "report": report_path,
        "violin_validation": violin_validation,
        "piano_validation": piano_validation,
        "violin_metrics": violin_metrics,
        "violin_stats": violin_stats,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Smooth violin Sky15 pipeline: latest Downloads MIDI -> smooth violin + piano Domiso txt."
    )
    parser.add_argument(
        "midi",
        nargs="?",
        help="Optional MIDI path or filename. If omitted, newest .mid/.midi in Downloads is used.",
    )
    parser.add_argument("--downloads", default=str(normal.default_downloads_dir()))
    parser.add_argument("--out-dir", default=str(ROOT_DIR / "txt"))
    parser.add_argument("--profile", default="auto", choices=["auto"] + sorted(sky.PROFILES))
    parser.add_argument("--violin-track", default="auto")
    parser.add_argument("--piano-tracks", default="auto")
    parser.add_argument("--violin-style", default="balanced", choices=sorted(PRESETS))
    parser.add_argument("--min-onset-ms", type=int, default=None)
    parser.add_argument("--piano-max-poly", default=4, type=int)
    parser.add_argument("--list", action="store_true", help="List recent MIDI files in Downloads and exit.")
    parser.add_argument("--analyze-only", action="store_true", help="Print selected tracks without writing txt files.")
    args = parser.parse_args()

    downloads = Path(args.downloads).expanduser()
    if args.list:
        for path in normal.list_download_midis(downloads):
            print(path)
        return

    input_path = normal.resolve_midi_path(args.midi, downloads)
    parsed = core.parse_midi(str(input_path))
    summaries = normal.build_track_summaries(parsed, normal.read_track_metadata(input_path))
    violin_track, piano_tracks, same_track_fallback = normal.choose_tracks(
        summaries,
        args.violin_track,
        args.piano_tracks,
    )
    if args.analyze_only:
        print(f"input={input_path}")
        normal.print_track_analysis(summaries, violin_track, piano_tracks)
        print(f"same_track_fallback={same_track_fallback}")
        print(f"smooth_style={args.violin_style}")
        print(f"preset={PRESETS[args.violin_style]}")
        return

    result = convert(args)
    vv: normal.ValidationResult = result["violin_validation"]  # type: ignore[assignment]
    pv: normal.ValidationResult = result["piano_validation"]  # type: ignore[assignment]
    print(f"input={result['input']}")
    print(f"profile={result['profile']}")
    print(f"smooth_style={result['style']}")
    print(f"tracks=violin:{result['violin_track']} piano:{','.join(str(t) for t in result['piano_tracks']) or 'fallback'}")
    print(f"transpose={result['transpose']}")
    print(f"smooth_violin={result['violin']}")
    print(f"smooth_piano={result['piano']}")
    print(f"analysis_report={result['report']}")
    print(f"violin_stats={result['violin_stats']}")
    print(f"violin_metrics={result['violin_metrics']}")
    if vv.available and pv.available:
        print(f"validation_violin=events:{vv.events} diagnostics:{vv.diagnostics} unmapped:{vv.unmapped}")
        print(f"validation_piano=events:{pv.events} diagnostics:{pv.diagnostics} unmapped:{pv.unmapped}")
    else:
        print(f"validation_skipped={vv.error or pv.error}")


if __name__ == "__main__":
    main()
