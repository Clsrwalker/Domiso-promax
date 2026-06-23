#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from typing import Dict, List, Tuple

import domiso_pipeline_literal as base
import domiso_pipeline_sky_melodylock as sky
import midi_to_domiso_dense3layer as core


PROFILES: Dict[str, sky.Profile] = {
    "sky_duet": sky.Profile(
        "sky_duet",
        "Sky duet: computer A plays the locked melody, computer B plays harmony and bass",
        -12,
        12,
        0.34,
        True,
        (0, -2, -1, 1, 2),
        1,
        3,
        0,
    ),
    "sky_duet_dense": sky.Profile(
        "sky_duet_dense",
        "Sky duet dense: keep the melody clear while allowing a fuller accompaniment on computer B",
        -12,
        12,
        0.26,
        True,
        (0, -3, -2, -1, 1, 2),
        2,
        4,
        0,
    ),
}


def recommend_profile(metrics: dict) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if metrics["max_poly"] >= 6 or metrics["bar_density_p90"] >= 16:
        reasons.append("dense source -> sky_duet_dense")
        return "sky_duet_dense", reasons
    reasons.append("default Sky duet profile")
    return "sky_duet", reasons


def next_duet_output_paths(out_dir: str, midi_base: str) -> Tuple[str, str]:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(out_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_domiso_script_sky_duet_([AB])_v(\d+)\.txt$",
        re.I,
    )
    max_v = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            max_v = max(max_v, int(m.group(2)))
    version = max_v + 1
    return (
        os.path.join(song_dir, f"{safe_base}_domiso_script_sky_duet_A_v{version}.txt"),
        os.path.join(song_dir, f"{safe_base}_domiso_script_sky_duet_B_v{version}.txt"),
    )


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_analysis_sky_duet_v(\d+)\.md$",
        re.I,
    )
    max_v = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            max_v = max(max_v, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_sky_duet_v{max_v + 1}.md")


def rest_tokens_for_steps(steps: int) -> List[str]:
    remaining = max(0, steps)
    tokens: List[str] = []
    while remaining > 0:
        for chunk_len, suffix in core.CHUNK_SUFFIX:
            if chunk_len <= remaining:
                tokens.append("0" + suffix)
                remaining -= chunk_len
                break
        else:
            raise RuntimeError(f"Could not render rest length: {remaining}")
    return tokens


def wrap_tokens(tokens: List[str], width: int = 120) -> List[str]:
    lines: List[str] = []
    current: List[str] = []
    for tok in tokens:
        current.append(tok)
        if len(" ".join(current)) > width:
            last = current.pop()
            if current:
                lines.append(" ".join(current))
            current = [last]
    if current:
        lines.append(" ".join(current))
    return lines


def build_part_text(
    *,
    midi_base: str,
    source_name: str,
    profile: sky.Profile,
    part: str,
    role: str,
    lines: List[str],
    initial_bpm: int,
    duration_s: float,
    count_in_steps: int,
    summary: str,
    stability: dict,
) -> str:
    count_in_tokens = rest_tokens_for_steps(count_in_steps)
    count_in_beats = count_in_steps / 4.0
    header = [
        f"Title: {midi_base.replace('-', ' ').replace('_', ' ').title()} (Sky Duet {part})",
        f"Source: {source_name}",
        f"Info: profile={profile.name}, {profile.desc}",
        f"Info: part={part}, role={role}",
        f"Info: count_in={count_in_beats:g} beats; start both computers together",
        f"Info: duration~{duration_s:.1f}s after count-in, grid 1/16",
        f"Info: dynamic transpose windows(4 bars): {summary}",
        f"Info: Sky 15-key layout C4-C6 -> {sky.SKY_LAYOUT}",
        (
            "Info: stability "
            f"peak_clusters/s={stability['clusters_per_sec_peak']}, "
            f"min_gap_ms={stability['min_cluster_gap_ms']}, "
            f"same_key_min_gap_ms={stability['same_key_min_gap_ms']}"
        ),
        "",
        f"bpm={initial_bpm}",
    ]
    if count_in_tokens:
        header.extend(["", "; Sync Count-In", *wrap_tokens(count_in_tokens)])
    header.extend(["", f"; Duet Part {part} {role}", *lines, ""])
    return "\n".join(header)


def lint_duet_text(text: str, marker: str) -> List[str]:
    issues: List[str] = []
    if re.search(r"(?<![A-Za-z0-9_])[+\-]*[1-7][#b](?![A-Za-z0-9_])", text):
        issues.append("Found accidental note tokens (#/b), expected Sky white-key mapping.")
    if marker not in text:
        issues.append(f"Missing section marker: {marker}")
    return issues


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str], extra: dict) -> None:
    lead_total = max(1, extra["lead_stats"]["lead_notes"])
    lead_track_ratio = extra["lead_stats"]["lead_from_melody_track"] / lead_total * 100.0
    lead_top_ratio = extra["lead_stats"]["lead_from_top_note"] / lead_total * 100.0
    lines = [
        f"# Analysis (Sky Duet Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Sky Duet Intent",
        "- output two synchronized txt files for two computers",
        "- Part A keeps the Sky melodylock lead as a stable monophonic melody",
        "- Part B combines harmony and bass, then applies a separate Sky input budget",
        "- both files start with the same silent count-in so operators can press play together",
        f"- target layout: {sky.SKY_LAYOUT}",
        "",
        "## Output Files",
        f"- part_a: {extra['output_a']}",
        f"- part_b: {extra['output_b']}",
        f"- count_in_beats: {extra['count_in_steps'] / 4.0:g}",
        "",
        "## Extraction Summary",
        f"- base_shift: {extra['base_shift']}",
        f"- dynamic_windows: {extra['summary']}",
        f"- lead_notes: {extra['lead_stats']['lead_notes']}",
        f"- lead_from_melody_track: {extra['lead_stats']['lead_from_melody_track']} ({lead_track_ratio:.1f}%)",
        f"- lead_from_top_note: {extra['lead_stats']['lead_from_top_note']} ({lead_top_ratio:.1f}%)",
        f"- fallback_lead_notes: {extra['lead_stats']['fallback_lead_notes']}",
        f"- raw_support_notes: {extra['raw_support_notes']}",
        f"- lead_speed_pruned: {extra['lead_speed_pruned']}",
        f"- support_notes_pruned: {extra['support_pruned']}",
        f"- part_a_budget_dropped: {extra['part_a_budget_dropped']}",
        f"- part_b_budget_dropped: {extra['part_b_budget_dropped']}",
        "",
        "## Input Stability",
        f"- part_a_clusters_per_sec_peak: {extra['stability_a']['clusters_per_sec_peak']}",
        f"- part_a_min_cluster_gap_ms: {extra['stability_a']['min_cluster_gap_ms']}",
        f"- part_a_same_key_min_gap_ms: {extra['stability_a']['same_key_min_gap_ms']}",
        f"- part_b_clusters_per_sec_peak: {extra['stability_b']['clusters_per_sec_peak']}",
        f"- part_b_min_cluster_gap_ms: {extra['stability_b']['min_cluster_gap_ms']}",
        f"- part_b_same_key_min_gap_ms: {extra['stability_b']['same_key_min_gap_ms']}",
        "",
        "## Playability",
        f"- part_a: {extra['play_a']['playable']}/{extra['play_a']['notes']} ({extra['play_a']['ratio']:.2f}%)",
        f"- part_b: {extra['play_b']['playable']}/{extra['play_b']['notes']} ({extra['play_b']['ratio']:.2f}%)",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def convert_midi(input_midi: str, out_dir: str, profile_name: str, count_in_beats: float = 4.0) -> dict:
    p = PROFILES[profile_name]
    parsed = core.parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)

    base_shift = sky.choose_base_shift_profile(notes, top_ids, parsed["melody_track"], tpb, p)
    shifts, win_ticks, changes = sky.choose_dynamic_shifts_profile(
        notes, top_ids, parsed["melody_track"], tpb, base_shift, p
    )
    tick_per_step = tpb / 4.0
    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    mapped, dist = sky.map_notes_sky(notes, shifts, win_ticks, tick_per_step)
    mapped = sky.annotate_mapped_notes(notes, mapped, top_ids, parsed["melody_track"])

    total_steps = max((n["end_step"] for n in mapped), default=0) + 1
    step_ms = sky.build_step_ms(total_steps, tempo_steps)

    lead_intervals, lead_ids, lead_stats = sky.extract_melody_intervals(mapped, parsed["melody_track"])
    lead_intervals, lead_speed_pruned = sky.prune_lead_for_input_speed(lead_intervals, step_ms)
    lead_pitch_by_step = sky.build_active_pitch_map(lead_intervals, total_steps)

    support_voices, support_pruned = sky.assign_support_voices(
        mapped, lead_ids, lead_pitch_by_step, parsed["melody_track"], parsed["bass_track"]
    )
    raw_support = base.merge_intervals_strict(support_voices["B"] + support_voices["C"])

    part_a, part_a_budget_dropped = sky.apply_input_budget_constraints(
        {"A": base.merge_intervals_strict(lead_intervals), "B": [], "C": []},
        step_ms,
    )
    part_b, part_b_budget_dropped = sky.apply_input_budget_constraints(
        {"A": [], "B": raw_support, "C": []},
        step_ms,
    )
    part_a_intervals = base.merge_intervals_strict(part_a["A"])
    part_b_intervals = base.merge_intervals_strict(part_b["B"])

    stability_a = sky.summarize_input_stability({"A": part_a_intervals, "B": [], "C": []}, step_ms)
    stability_b = sky.summarize_input_stability({"A": [], "B": part_b_intervals, "C": []}, step_ms)

    seg_a = base.intervals_to_segments_limited(part_a_intervals, total_steps, 1)
    seg_b = base.intervals_to_segments_limited(part_b_intervals, total_steps, p.b_max_poly)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)

    midi_base = os.path.splitext(os.path.basename(input_midi))[0]
    out_a, out_b = next_duet_output_paths(out_dir, midi_base)
    summary = core.summarize_windows(shifts)
    duration = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    count_in_steps = max(0, int(round(count_in_beats * 4.0)))

    text_a = build_part_text(
        midi_base=midi_base,
        source_name=os.path.basename(input_midi),
        profile=p,
        part="A",
        role="Melody",
        lines=lines_a,
        initial_bpm=tempos[0][1],
        duration_s=duration,
        count_in_steps=count_in_steps,
        summary=summary,
        stability=stability_a,
    )
    text_b = build_part_text(
        midi_base=midi_base,
        source_name=os.path.basename(input_midi),
        profile=p,
        part="B",
        role="Harmony+Bass",
        lines=lines_b,
        initial_bpm=tempos[0][1],
        duration_s=duration,
        count_in_steps=count_in_steps,
        summary=summary,
        stability=stability_b,
    )

    issues = lint_duet_text(text_a, "; Duet Part A Melody") + lint_duet_text(text_b, "; Duet Part B Harmony+Bass")
    if issues:
        raise RuntimeError(" | ".join(issues))

    with open(out_a, "w", encoding="utf-8", newline="\n") as f:
        f.write(text_a)
    with open(out_b, "w", encoding="utf-8", newline="\n") as f:
        f.write(text_b)

    play_a = sky.evaluate_txt_playability(out_a)
    play_b = sky.evaluate_txt_playability(out_b)
    return {
        "outputs": [out_a, out_b],
        "output_a": out_a,
        "output_b": out_b,
        "profile": p.name,
        "notes": len(notes),
        "base_shift": base_shift,
        "changes": changes,
        "summary": summary,
        "dist": round(dist, 2),
        "count_in_steps": count_in_steps,
        "lead_stats": lead_stats,
        "raw_support_notes": len(raw_support),
        "lead_speed_pruned": lead_speed_pruned,
        "support_pruned": support_pruned,
        "part_a_budget_dropped": part_a_budget_dropped,
        "part_b_budget_dropped": part_b_budget_dropped,
        "stability_a": stability_a,
        "stability_b": stability_b,
        "play_a": play_a,
        "play_b": play_b,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate synchronized Sky 15-key MelodyLock duet txt files for two computers."
    )
    sub = ap.add_subparsers(dest="cmd")

    ap_an = sub.add_parser("analyze")
    ap_an.add_argument("input_midi")
    ap_an.add_argument("--json", action="store_true")

    ap_cv = sub.add_parser("convert")
    ap_cv.add_argument("input_midi")
    ap_cv.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_cv.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    ap_cv.add_argument("--count-in-beats", type=float, default=4.0)

    ap_pl = sub.add_parser("pipeline")
    ap_pl.add_argument("input_midi")
    ap_pl.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--report-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    ap_pl.add_argument("--count-in-beats", type=float, default=4.0)

    ap_cp = sub.add_parser("compare")
    ap_cp.add_argument("file_a")
    ap_cp.add_argument("file_b")

    args = ap.parse_args()

    if args.cmd == "analyze":
        parsed = core.parse_midi(args.input_midi)
        metrics = sky.analyze_midi(parsed)
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
        metrics = sky.analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, profile, args.count_in_beats)
        print(f"output_a={res['output_a']}")
        print(f"output_b={res['output_b']}")
        print(f"profile={res['profile']}")
        if reasons:
            print(f"profile_reasons={'; '.join(reasons)}")
        print(
            "playability="
            f"A {res['play_a']['playable']}/{res['play_a']['notes']} ({res['play_a']['ratio']:.2f}%), "
            f"B {res['play_b']['playable']}/{res['play_b']['notes']} ({res['play_b']['ratio']:.2f}%)"
        )
        return

    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        metrics = sky.analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, profile, args.count_in_beats)
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(report, args.input_midi, metrics, profile, reasons, res)
        print(f"output_a={res['output_a']}")
        print(f"output_b={res['output_b']}")
        print(f"analysis_report={report}")
        print(f"profile={profile}")
        print(
            "playability="
            f"A {res['play_a']['playable']}/{res['play_a']['notes']} ({res['play_a']['ratio']:.2f}%), "
            f"B {res['play_b']['playable']}/{res['play_b']['notes']} ({res['play_b']['ratio']:.2f}%)"
        )
        return

    if args.cmd == "compare":
        pa = sky.evaluate_txt_playability(args.file_a)
        pb = sky.evaluate_txt_playability(args.file_b)
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

    legacy = argparse.ArgumentParser(description="legacy Sky duet convert")
    legacy.add_argument("input_midi")
    legacy.add_argument("--out-dir", default=r"d:\domiso\txt")
    legacy.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    legacy.add_argument("--count-in-beats", type=float, default=4.0)
    largs = legacy.parse_args()
    parsed = core.parse_midi(largs.input_midi)
    metrics = sky.analyze_midi(parsed)
    profile, _ = recommend_profile(metrics) if largs.profile == "auto" else (largs.profile, [])
    res = convert_midi(largs.input_midi, largs.out_dir, profile, largs.count_in_beats)
    print(f"output_a={res['output_a']}")
    print(f"output_b={res['output_b']}")
    print(f"profile={res['profile']}")
    print(
        "playability="
        f"A {res['play_a']['playable']}/{res['play_a']['notes']} ({res['play_a']['ratio']:.2f}%), "
        f"B {res['play_b']['playable']}/{res['play_b']['notes']} ({res['play_b']['ratio']:.2f}%)"
    )


if __name__ == "__main__":
    main()
