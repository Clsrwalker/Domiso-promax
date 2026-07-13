#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterable

import domiso_pipeline_literal as base
import domiso_pipeline_literal_melodylock as melodylock
import midi_to_domiso_dense3layer as core


ROOT_DIR = Path(__file__).resolve().parent.parent
MIDI_EXTS = (".mid", ".midi")


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
            candidates.extend(downloads / f"{value}{ext}" for ext in MIDI_EXTS)
        for path in candidates:
            if path.exists() and path.is_file():
                return path.resolve()
        raise SystemExit(f"MIDI not found. Tried path/name under Downloads: {value}")

    recent = list_download_midis(downloads, limit=1)
    if not recent:
        raise SystemExit(f"No .mid/.midi files found in {downloads}")
    return recent[0].resolve()


def next_ensemble_paths(out_dir: Path, midi_stem: str) -> tuple[Path, Path, Path, int]:
    safe_base = core.normalize_output_base(midi_stem)
    song_dir = out_dir / safe_base
    song_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(
        re.escape(safe_base)
        + r"_(?:domiso_script_literal_melodylock_ensemble_[AB]|analysis_literal_melodylock_ensemble)_v(\d+)\.(?:txt|md)$",
        re.I,
    )
    max_version = 0
    for child in song_dir.iterdir():
        match = pattern.match(child.name)
        if match:
            max_version = max(max_version, int(match.group(1)))
    version = max_version + 1
    part_a = song_dir / f"{safe_base}_domiso_script_literal_melodylock_ensemble_A_v{version}.txt"
    part_b = song_dir / f"{safe_base}_domiso_script_literal_melodylock_ensemble_B_v{version}.txt"
    report = song_dir / f"{safe_base}_analysis_literal_melodylock_ensemble_v{version}.md"
    return part_a, part_b, report, version


def rest_tokens_for_steps(steps: int) -> list[str]:
    remaining = max(0, steps)
    tokens: list[str] = []
    while remaining > 0:
        for chunk_len, suffix in core.CHUNK_SUFFIX:
            if chunk_len <= remaining:
                tokens.append("0" + suffix)
                remaining -= chunk_len
                break
        else:
            raise RuntimeError(f"Could not render rest length: {remaining}")
    return tokens


def wrap_tokens(tokens: Iterable[str], width: int = 120) -> list[str]:
    lines: list[str] = []
    current: list[str] = []
    for token in tokens:
        current.append(token)
        if len(" ".join(current)) > width:
            last = current.pop()
            if current:
                lines.append(" ".join(current))
            current = [last]
    if current:
        lines.append(" ".join(current))
    return lines


def render_part_text(
    *,
    midi_stem: str,
    source_name: str,
    profile: melodylock.Profile,
    part: str,
    role: str,
    lines: list[str],
    initial_bpm: int,
    duration_s: float,
    count_in_steps: int,
    shift_summary: str,
    max_poly: int,
) -> str:
    title = midi_stem.replace("-", " ").replace("_", " ").strip().title()
    count_in_beats = count_in_steps / 4.0
    header = [
        f"Title: {title} (Literal MelodyLock Ensemble {part})",
        f"Source: {source_name}",
        f"Info: profile={profile.name}, {profile.desc}",
        f"Info: part={part}, role={role}, max_poly={max_poly}",
        f"Info: count_in={count_in_beats:g} beats; start both parts together",
        f"Info: duration~{duration_s:.1f}s after count-in, grid=sixteenth",
        f"Info: dynamic transpose windows(4 bars): {shift_summary}",
        "",
        f"bpm={initial_bpm}",
    ]
    count_in_tokens = rest_tokens_for_steps(count_in_steps)
    if count_in_tokens:
        header.extend(["", "; Sync Count-In", *wrap_tokens(count_in_tokens)])
    header.extend(["", f"; Ensemble Part {part} {role}", *lines, ""])
    return "\n".join(header)


def lint_part_text(text: str, marker: str) -> list[str]:
    issues: list[str] = []
    if re.search(r"(?<![A-Za-z0-9_])[+\-]*[1-7][#b](?![A-Za-z0-9_])", text):
        issues.append("Found accidental note tokens (#/b), expected white-key-only mapping.")
    if marker not in text:
        issues.append(f"Missing section marker: {marker}")
    return issues


def build_ensemble_parts(
    input_midi: Path,
    profile_name: str,
    support_max_poly_arg: int,
) -> dict[str, object]:
    profile = melodylock.PROFILES[profile_name]
    parsed = core.parse_midi(str(input_midi))
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)

    base_shift = melodylock.choose_base_shift_profile(
        notes, top_ids, parsed["melody_track"], tpb, profile
    )
    shifts, window_ticks, shift_changes = melodylock.choose_dynamic_shifts_profile(
        notes, top_ids, parsed["melody_track"], tpb, base_shift, profile
    )

    tick_per_step = tpb / 4.0
    mapped, dist = core.map_notes(notes, shifts, window_ticks, tick_per_step)
    mapped = melodylock.annotate_mapped_notes(
        notes, mapped, top_ids, parsed["melody_track"]
    )

    lead_intervals, lead_ids, lead_stats = melodylock.extract_melody_intervals(
        mapped, parsed["melody_track"]
    )
    total_steps = max((n["end_step"] for n in mapped), default=0) + 1
    lead_pitch_by_step = melodylock.build_active_pitch_map(lead_intervals, total_steps)

    support_voices, support_pruned = melodylock.assign_support_voices(
        mapped,
        lead_ids,
        lead_pitch_by_step,
        parsed["melody_track"],
        parsed["bass_track"],
    )

    part_a_intervals = base.merge_intervals_strict(lead_intervals)
    raw_support = support_voices["B"] + support_voices["C"]
    part_b_intervals = base.merge_intervals_strict(raw_support)
    support_max_poly = support_max_poly_arg
    if support_max_poly <= 0:
        support_max_poly = max(1, min(8, profile.b_max_poly + profile.c_max_poly))

    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    seg_a = base.intervals_to_segments_limited(part_a_intervals, total_steps, 1)
    seg_b = base.intervals_to_segments_limited(
        part_b_intervals,
        total_steps,
        support_max_poly,
    )
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)

    return {
        "profile": profile,
        "parsed": parsed,
        "tempos": tempos,
        "tempo_steps": tempo_steps,
        "base_shift": base_shift,
        "shift_changes": shift_changes,
        "shift_summary": core.summarize_windows(shifts),
        "dist": round(dist, 2),
        "total_steps": total_steps,
        "duration_s": core.tick_to_seconds(parsed["max_tick"], tempos, tpb),
        "part_a_intervals": part_a_intervals,
        "part_b_intervals": part_b_intervals,
        "part_a_lines": lines_a,
        "part_b_lines": lines_b,
        "support_max_poly": support_max_poly,
        "lead_stats": lead_stats,
        "support_pruned": support_pruned,
        "raw_support_notes": len(raw_support),
    }


def write_report(
    path: Path,
    *,
    input_path: Path,
    metrics: dict,
    profile_name: str,
    reasons: list[str],
    result: dict[str, object],
    part_a_path: Path,
    part_b_path: Path,
    play_a: dict,
    play_b: dict,
    version: int,
    count_in_beats: float,
) -> None:
    lead_stats = result["lead_stats"]
    assert isinstance(lead_stats, dict)
    lead_total = max(1, int(lead_stats["lead_notes"]))
    lead_track_ratio = int(lead_stats["lead_from_melody_track"]) / lead_total * 100.0
    lead_top_ratio = int(lead_stats["lead_from_top_note"]) / lead_total * 100.0
    lines = [
        f"# Analysis (Literal MelodyLock Ensemble): {input_path.name}",
        "",
        "## Metrics",
        *[f"- {key}: {value}" for key, value in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile_name}",
        *[f"- reason: {reason}" for reason in reasons],
        "",
        "## Ensemble Intent",
        "- output two synchronized txt files for two Domiso players/computers",
        "- Part A keeps the melodylock lead as one clear melodic line",
        "- Part B combines the original Harmony and Bass support from literal_melodylock",
        "- both parts use the same transpose windows and tempo map",
        f"- count_in_beats: {count_in_beats:g}",
        "",
        "## Output Files",
        f"- part_a: {part_a_path}",
        f"- part_b: {part_b_path}",
        f"- version: {version}",
        "",
        "## Mapping",
        f"- base_shift: {result['base_shift']}",
        f"- dynamic_windows: {result['shift_summary']}",
        f"- shift_changes: {result['shift_changes']}",
        f"- distance: {result['dist']}",
        f"- support_max_poly: {result['support_max_poly']}",
        "",
        "## Extraction",
        f"- lead_notes: {lead_stats['lead_notes']}",
        f"- lead_from_melody_track: {lead_stats['lead_from_melody_track']} ({lead_track_ratio:.1f}%)",
        f"- lead_from_top_note: {lead_stats['lead_from_top_note']} ({lead_top_ratio:.1f}%)",
        f"- fallback_lead_notes: {lead_stats['fallback_lead_notes']}",
        f"- raw_support_notes: {result['raw_support_notes']}",
        f"- support_pruned: {result['support_pruned']}",
        "",
        "## Playability",
        f"- part_a: {play_a['playable']}/{play_a['notes']} ({play_a['ratio']:.2f}%)",
        f"- part_b: {play_b['playable']}/{play_b['notes']} ({play_b['ratio']:.2f}%)",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def convert(args: argparse.Namespace) -> dict[str, object]:
    downloads = Path(args.downloads).expanduser()
    input_path = resolve_midi_path(args.midi, downloads)
    parsed_for_metrics = core.parse_midi(str(input_path))
    metrics = melodylock.analyze_midi(parsed_for_metrics)
    if args.profile == "auto":
        profile_name, reasons = melodylock.recommend_profile(metrics)
    else:
        profile_name, reasons = args.profile, []

    result = build_ensemble_parts(input_path, profile_name, int(args.support_max_poly))
    profile = result["profile"]
    assert isinstance(profile, melodylock.Profile)

    out_dir = Path(args.out_dir).expanduser()
    part_a_path, part_b_path, report_path, version = next_ensemble_paths(
        out_dir, input_path.stem
    )
    count_in_steps = max(0, int(round(float(args.count_in_beats) * 4.0)))
    text_a = render_part_text(
        midi_stem=input_path.stem,
        source_name=input_path.name,
        profile=profile,
        part="A",
        role="Melody Lead",
        lines=result["part_a_lines"],  # type: ignore[arg-type]
        initial_bpm=int(result["tempos"][0][1]),  # type: ignore[index]
        duration_s=float(result["duration_s"]),
        count_in_steps=count_in_steps,
        shift_summary=str(result["shift_summary"]),
        max_poly=1,
    )
    text_b = render_part_text(
        midi_stem=input_path.stem,
        source_name=input_path.name,
        profile=profile,
        part="B",
        role="Harmony And Bass",
        lines=result["part_b_lines"],  # type: ignore[arg-type]
        initial_bpm=int(result["tempos"][0][1]),  # type: ignore[index]
        duration_s=float(result["duration_s"]),
        count_in_steps=count_in_steps,
        shift_summary=str(result["shift_summary"]),
        max_poly=int(result["support_max_poly"]),
    )

    issues = lint_part_text(text_a, "; Ensemble Part A Melody Lead")
    issues.extend(lint_part_text(text_b, "; Ensemble Part B Harmony And Bass"))
    if issues:
        raise RuntimeError(" | ".join(issues))

    part_a_path.write_text(text_a, encoding="utf-8", newline="\n")
    part_b_path.write_text(text_b, encoding="utf-8", newline="\n")
    play_a = base.evaluate_txt_playability(str(part_a_path))
    play_b = base.evaluate_txt_playability(str(part_b_path))
    write_report(
        report_path,
        input_path=input_path,
        metrics=metrics,
        profile_name=profile_name,
        reasons=reasons,
        result=result,
        part_a_path=part_a_path,
        part_b_path=part_b_path,
        play_a=play_a,
        play_b=play_b,
        version=version,
        count_in_beats=float(args.count_in_beats),
    )

    return {
        "input": input_path,
        "part_a": part_a_path,
        "part_b": part_b_path,
        "report": report_path,
        "version": version,
        "profile": profile_name,
        "play_a": play_a,
        "play_b": play_b,
        "shift_summary": result["shift_summary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Literal MelodyLock ensemble A/B Domiso txt files."
    )
    parser.add_argument(
        "midi",
        nargs="?",
        help="Optional MIDI path or filename. If omitted, newest .mid/.midi in Downloads is used.",
    )
    parser.add_argument("--downloads", default=str(default_downloads_dir()))
    parser.add_argument("--out-dir", default=str(ROOT_DIR / "txt"))
    parser.add_argument("--profile", default="auto", choices=["auto"] + sorted(melodylock.PROFILES))
    parser.add_argument(
        "--count-in-beats",
        type=float,
        default=4.0,
        help="Silent count-in inserted before both parts.",
    )
    parser.add_argument(
        "--support-max-poly",
        type=int,
        default=0,
        help="Part B max simultaneous notes; 0 uses the profile default.",
    )
    parser.add_argument("--list", action="store_true", help="List recent MIDI files in Downloads and exit.")
    parser.add_argument("--analyze-only", action="store_true", help="Print profile decision without writing txt files.")
    parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    args = parser.parse_args()

    downloads = Path(args.downloads).expanduser()
    if args.list:
        for path in list_download_midis(downloads):
            print(path)
        return

    input_path = resolve_midi_path(args.midi, downloads)
    if args.analyze_only:
        parsed = core.parse_midi(str(input_path))
        metrics = melodylock.analyze_midi(parsed)
        profile, reasons = melodylock.recommend_profile(metrics)
        data = {
            "input": str(input_path),
            "recommended_profile": profile,
            "reasons": reasons,
            "metrics": metrics,
        }
        print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else data)
        return

    args.midi = str(input_path)
    result = convert(args)
    if args.json:
        print(
            json.dumps(
                {
                    "input": str(result["input"]),
                    "profile": result["profile"],
                    "part_a": str(result["part_a"]),
                    "part_b": str(result["part_b"]),
                    "analysis_report": str(result["report"]),
                    "transpose": result["shift_summary"],
                    "play_a": result["play_a"],
                    "play_b": result["play_b"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    play_a = result["play_a"]
    play_b = result["play_b"]
    print(f"input={result['input']}")
    print(f"profile={result['profile']}")
    print(f"transpose={result['shift_summary']}")
    print(f"part_a={result['part_a']}")
    print(f"part_b={result['part_b']}")
    print(f"analysis_report={result['report']}")
    print(
        "playability="
        f"A {play_a['playable']}/{play_a['notes']} ({play_a['ratio']:.2f}%), "
        f"B {play_b['playable']}/{play_b['notes']} ({play_b['ratio']:.2f}%)"
    )


if __name__ == "__main__":
    main()
