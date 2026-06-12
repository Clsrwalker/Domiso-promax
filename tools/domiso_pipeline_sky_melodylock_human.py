#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

import domiso_pipeline_literal as base
import domiso_pipeline_longnote_human_v2 as human
import domiso_pipeline_sky_melodylock as sky
import midi_to_domiso_dense3layer as core


@dataclass(frozen=True)
class HumanMode:
    name: str
    desc: str
    rubato_depth: int
    delay_steps: int
    support_lag_ratio: float
    pocket_ratio: float
    release_ratio: float
    breath_every_steps: int
    breath_gap_steps: int
    use_pocket: bool


PROFILES: Dict[str, sky.Profile] = {
    "sky_melodylock_human": sky.Profile(
        "sky_melodylock_human",
        "Sky 15-key melodylock human: keep the hook centered, then add subtle breath, lag and rubato",
        -12,
        12,
        0.34,
        True,
        (0, -2, -1, 1, 2),
        1,
        3,
        1,
    ),
    "sky_melodylock_human_dense": sky.Profile(
        "sky_melodylock_human_dense",
        "Sky 15-key melodylock human dense: preserve more body, but still shape timing like a player",
        -12,
        12,
        0.26,
        True,
        (0, -3, -2, -1, 1, 2),
        2,
        4,
        1,
    ),
}


HUMAN_MODES: Dict[str, HumanMode] = {
    "lite": HumanMode(
        "lite",
        "minimal humanization for Sky stability",
        rubato_depth=1,
        delay_steps=1,
        support_lag_ratio=0.24,
        pocket_ratio=0.0,
        release_ratio=0.10,
        breath_every_steps=28,
        breath_gap_steps=1,
        use_pocket=False,
    ),
    "full": HumanMode(
        "full",
        "subtle phrase rubato + support lag + light back/front pocket",
        rubato_depth=2,
        delay_steps=1,
        support_lag_ratio=0.34,
        pocket_ratio=0.16,
        release_ratio=0.18,
        breath_every_steps=24,
        breath_gap_steps=1,
        use_pocket=True,
    ),
}


def recommend_profile(metrics: dict) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if metrics["max_poly"] >= 6 or metrics["bar_density_p90"] >= 16:
        reasons.append("15-key range + dense source -> sky_melodylock_human_dense")
        return "sky_melodylock_human_dense", reasons
    reasons.append("default Sky melodylock human profile")
    return "sky_melodylock_human", reasons


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_analysis_sky_melodylock_human_v(\d+)\.md$",
        re.I,
    )
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_sky_melodylock_human_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str], extra: dict) -> None:
    lead_total = max(1, extra["lead_stats"]["lead_notes"])
    lead_track_ratio = extra["lead_stats"]["lead_from_melody_track"] / lead_total * 100.0
    lead_top_ratio = extra["lead_stats"]["lead_from_top_note"] / lead_total * 100.0
    lines = [
        f"# Analysis (Sky MelodyLock Human Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Sky MelodyLock Human Intent",
        "- keep Sky melodylock's recognizable top line and thin support structure",
        "- add only light human timing, because Sky has tighter playable input limits than the 21-key scripts",
        "- use phrase breath on melody, support lag behind the hook, short weak-tail release, and gradual rubato",
        f"- target layout: {sky.SKY_LAYOUT}",
        "",
        "## Extraction Summary",
        f"- human_mode: {extra['human_mode']}",
        f"- human_desc: {extra['human_desc']}",
        f"- base_shift: {extra['base_shift']}",
        f"- dynamic_windows: {extra['summary']}",
        f"- lead_notes: {extra['lead_stats']['lead_notes']}",
        f"- lead_from_melody_track: {extra['lead_stats']['lead_from_melody_track']} ({lead_track_ratio:.1f}%)",
        f"- lead_from_top_note: {extra['lead_stats']['lead_from_top_note']} ({lead_top_ratio:.1f}%)",
        f"- fallback_lead_notes: {extra['lead_stats']['fallback_lead_notes']}",
        f"- lead_speed_pruned: {extra['lead_speed_pruned']}",
        f"- support_notes_pruned: {extra['support_pruned']}",
        f"- input_budget_dropped: {extra['input_budget_dropped']}",
        "",
        "## Humanization Summary",
        f"- breath_hits: {extra['breath_hits']}",
        f"- lag_hits: {extra['lag_hits']}",
        f"- pocket_hits: {extra['pocket_hits']}",
        f"- release_hits: {extra['release_hits']}",
        f"- rubato_depth_bpm: {extra['rubato_depth']}",
        "",
        "## Input Stability",
        f"- clusters_per_sec_peak: {extra['stability']['clusters_per_sec_peak']}",
        f"- min_cluster_gap_ms: {extra['stability']['min_cluster_gap_ms']}",
        f"- same_key_min_gap_ms: {extra['stability']['same_key_min_gap_ms']}",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def convert_midi(
    input_midi: str,
    out_dir: str,
    profile_name: str,
    humanize: bool = True,
    human_mode: str = "lite",
) -> dict:
    p = PROFILES[profile_name]
    mode = HUMAN_MODES[(human_mode or "lite").lower()]
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

    lead_intervals, lead_ids, lead_stats = sky.extract_melody_intervals(mapped, parsed["melody_track"])
    total_steps = max(n["end_step"] for n in mapped) + 1 if mapped else 0
    step_ms = sky.build_step_ms(total_steps, tempo_steps)
    lead_intervals, lead_speed_pruned = sky.prune_lead_for_input_speed(lead_intervals, step_ms)
    lead_pitch_by_step = sky.build_active_pitch_map(lead_intervals, total_steps)

    support_voices, support_pruned = sky.assign_support_voices(
        mapped, lead_ids, lead_pitch_by_step, parsed["melody_track"], parsed["bass_track"]
    )

    merged = {
        "A": base.merge_intervals_strict(lead_intervals),
        "B": base.merge_intervals_strict(support_voices["B"]),
        "C": base.merge_intervals_strict(support_voices["C"]),
    }

    density = human.classify_density_windows(mapped, human.build_window_steps())
    pocket_windows = human.build_pocket_windows(density, tempos[0][1])

    breath_hits = 0
    lag_hits = 0
    pocket_hits = 0
    release_hits = 0
    rubato_depth = 0
    tempo_steps_out = tempo_steps
    if humanize:
        merged["A"], breath_hits = human.apply_melody_breath(
            merged["A"],
            mode.breath_every_steps,
            mode.breath_gap_steps,
            jump_trigger=9,
        )
        melody_starts = {s for s, _, _ in merged["A"]}
        merged["B"], lag_b = human.apply_support_lag(
            merged["B"],
            melody_starts,
            mode.delay_steps,
            mode.support_lag_ratio,
        )
        bass_delay = 1 if mode.delay_steps > 0 else 0
        merged["C"], lag_c = human.apply_support_lag(
            merged["C"],
            melody_starts,
            bass_delay,
            mode.support_lag_ratio * 0.45,
        )
        lag_hits = lag_b + lag_c
        if mode.use_pocket:
            merged["B"], pocket_b = human.apply_pocket(
                merged["B"],
                pocket_windows,
                human.build_window_steps(),
                mode.pocket_ratio,
            )
            merged["C"], pocket_c = human.apply_pocket(
                merged["C"],
                pocket_windows,
                human.build_window_steps(),
                mode.pocket_ratio * 0.45,
            )
            pocket_hits = pocket_b + pocket_c
        merged["B"], rel_b = human.apply_human_release(merged["B"], mode.release_ratio)
        merged["C"], rel_c = human.apply_human_release(merged["C"], mode.release_ratio * 0.55)
        release_hits = rel_b + rel_c
        phrase_ranges = human.build_phrase_ranges(merged["A"])
        rubato_depth = mode.rubato_depth
        tempo_steps_out = human.build_rubato_tempo_steps(tempo_steps, phrase_ranges, rubato_depth)

    step_ms_out = sky.build_step_ms(total_steps, tempo_steps_out)
    merged, input_budget_dropped = sky.apply_input_budget_constraints(merged, step_ms_out)
    stability = sky.summarize_input_stability(merged, step_ms_out)

    seg_a = base.intervals_to_segments_limited(merged["A"], total_steps, 1)
    seg_b = base.intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = base.intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)
    lines_a = core.serialize_voice(seg_a, tempo_steps_out)
    lines_b = core.serialize_voice(seg_b, tempo_steps_out)
    lines_c = core.serialize_voice(seg_c, tempo_steps_out)

    midi_base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = base.next_script_output_path(out_dir, midi_base, "script_sky_melodylock_human")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    text = "\n".join(
        [
            f"Title: {midi_base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
            f"Source: {os.path.basename(input_midi)}",
            f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
            f"Info: profile={p.name}, {p.desc}",
            f"Info: dynamic transpose windows(4 bars): {summary}",
            f"Info: Sky 15-key layout C4-C6 -> {sky.SKY_LAYOUT}",
            (
                "Info: humanize=on "
                f"mode={mode.name}, rubato+/-{rubato_depth}bpm gradual, "
                f"breath={breath_hits}, lag={lag_hits}, pocket={pocket_hits}, release={release_hits}"
            )
            if humanize
            else "Info: humanize=off",
            (
                "Info: speed_guard "
                f"lead_pruned={lead_speed_pruned}, support_pruned={support_pruned}, "
                f"input_budget_dropped={input_budget_dropped}, "
                f"peak_clusters/s={stability['clusters_per_sec_peak']}"
            ),
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
    )

    issues = core.lint_domiso_text(text)
    if issues:
        raise RuntimeError(" | ".join(issues))
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    play = sky.evaluate_txt_playability(out_path)
    return {
        "output": out_path,
        "profile": p.name,
        "notes": len(notes),
        "base_shift": base_shift,
        "changes": changes,
        "summary": summary,
        "dist": round(dist, 2),
        "play": play,
        "humanize": humanize,
        "human_mode": mode.name,
        "human_desc": mode.desc,
        "rubato_depth": rubato_depth,
        "lead_stats": lead_stats,
        "lead_speed_pruned": lead_speed_pruned,
        "support_pruned": support_pruned,
        "input_budget_dropped": input_budget_dropped,
        "stability": stability,
        "breath_hits": breath_hits,
        "lag_hits": lag_hits,
        "pocket_hits": pocket_hits,
        "release_hits": release_hits,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Analyze + profile-select + Sky 15-key melodylock human DoMiSo conversion workflow."
    )
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
    ap_cv.add_argument("--human-mode", default="lite", choices=sorted(HUMAN_MODES))

    ap_pl = sub.add_parser("pipeline")
    ap_pl.add_argument("input_midi")
    ap_pl.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--report-dir", default=r"d:\domiso\txt")
    ap_pl.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    ap_pl.set_defaults(humanize=True)
    ap_pl.add_argument("--no-humanize", action="store_false", dest="humanize")
    ap_pl.add_argument("--human-mode", default="lite", choices=sorted(HUMAN_MODES))

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
            "human_modes": {k: v.desc for k, v in HUMAN_MODES.items()},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else out)
        return

    if args.cmd == "convert":
        parsed = core.parse_midi(args.input_midi)
        metrics = sky.analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(
            args.input_midi,
            args.out_dir,
            profile,
            humanize=args.humanize,
            human_mode=args.human_mode,
        )
        print(f"output={res['output']}")
        print(f"profile={res['profile']}")
        print(f"humanize={'on' if res['humanize'] else 'off'}")
        print(f"human_mode={res['human_mode']}")
        if reasons:
            print(f"profile_reasons={'; '.join(reasons)}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        metrics = sky.analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(
            args.input_midi,
            args.out_dir,
            profile,
            humanize=args.humanize,
            human_mode=args.human_mode,
        )
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(
            report,
            args.input_midi,
            metrics,
            profile,
            reasons,
            {
                "human_mode": res["human_mode"],
                "human_desc": res["human_desc"],
                "base_shift": res["base_shift"],
                "summary": res["summary"],
                "lead_stats": res["lead_stats"],
                "lead_speed_pruned": res["lead_speed_pruned"],
                "support_pruned": res["support_pruned"],
                "input_budget_dropped": res["input_budget_dropped"],
                "stability": res["stability"],
                "breath_hits": res["breath_hits"],
                "lag_hits": res["lag_hits"],
                "pocket_hits": res["pocket_hits"],
                "release_hits": res["release_hits"],
                "rubato_depth": res["rubato_depth"],
            },
        )
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={profile}")
        print(f"humanize={'on' if res['humanize'] else 'off'}")
        print(f"human_mode={res['human_mode']}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
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

    legacy = argparse.ArgumentParser(description="legacy convert")
    legacy.add_argument("input_midi")
    legacy.add_argument("--out-dir", default=r"d:\domiso\txt")
    legacy.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    legacy.set_defaults(humanize=True)
    legacy.add_argument("--no-humanize", action="store_false", dest="humanize")
    legacy.add_argument("--human-mode", default="lite", choices=sorted(HUMAN_MODES))
    largs = legacy.parse_args()
    parsed = core.parse_midi(largs.input_midi)
    metrics = sky.analyze_midi(parsed)
    profile, _ = recommend_profile(metrics) if largs.profile == "auto" else (largs.profile, [])
    res = convert_midi(
        largs.input_midi,
        largs.out_dir,
        profile,
        humanize=largs.humanize,
        human_mode=largs.human_mode,
    )
    print(f"output={res['output']}")
    print(f"profile={res['profile']}")
    print(f"humanize={'on' if res['humanize'] else 'off'}")
    print(f"human_mode={res['human_mode']}")
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")


if __name__ == "__main__":
    main()
