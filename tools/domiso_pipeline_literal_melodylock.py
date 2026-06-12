#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import domiso_pipeline_literal as base
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
    b_max_poly: int
    c_max_poly: int


PROFILES: Dict[str, Profile] = {
    "literal_melodylock": Profile(
        "literal_melodylock",
        "melody-locked literal mapping: monophonic lead, restrained support, less chord-smear",
        -12,
        12,
        0.18,
        True,
        (0, -2, -1, 1, 2),
        1,
        6,
        2,
    ),
    "literal_melodylock_dense": Profile(
        "literal_melodylock_dense",
        "dense melody-locked literal mapping: preserve more source body while keeping lead singable",
        -12,
        12,
        0.12,
        True,
        (0, -2, -1, 1, 2),
        1,
        8,
        2,
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
    if metrics["max_poly"] >= 7 or metrics["bar_density_p90"] >= 18:
        reasons.append("dense piano texture -> literal_melodylock_dense")
        return "literal_melodylock_dense", reasons
    reasons.append("default melody-locked literal profile")
    return "literal_melodylock", reasons


def choose_base_shift_profile(
    notes: List[dict], top_ids: set, melody_track: int, tpb: int, p: Profile
) -> int:
    best_s, best_c = 0, float("inf")
    for s in range(p.shift_min, p.shift_max + 1):
        c = core.evaluate_shift_cost(notes, s, top_ids, melody_track, tpb) + p.shift_bias * abs(s)
        if c < best_c:
            best_s, best_c = s, c
    return best_s


def choose_dynamic_shifts_profile(
    notes: List[dict], top_ids: set, melody_track: int, tpb: int, base_shift: int, p: Profile
) -> Tuple[List[int], int, int]:
    win_ticks = max(1, tpb * 16)
    max_win = max(n["start"] // win_ticks for n in notes)
    cnt = max_win + 1
    if not p.dynamic:
        return [base_shift] * cnt, win_ticks, 0

    cands = sorted(
        {base_shift + d for d in p.dynamic_offsets if p.shift_min <= base_shift + d <= p.shift_max}
        | {base_shift}
    )
    by_w = defaultdict(list)
    for i, n in enumerate(notes):
        by_w[n["start"] // win_ticks].append((i, n))

    local_costs = []
    for w in range(cnt):
        entries = by_w.get(w, [])
        vals = {}
        for shift in cands:
            total = 0.0
            for gi, n in entries:
                _, dist = core.fold_and_snap(n["note"] + shift)
                weight = 1.0
                if gi in top_ids:
                    weight += 0.8
                if n["track"] == melody_track:
                    weight += 0.35
                total += dist * weight
            vals[shift] = total
        local_costs.append(vals)

    dp = {(shift, 0): local_costs[0][shift] for shift in cands}
    back = [{(shift, 0): None for shift in cands}]
    for w in range(1, cnt):
        ndp = {}
        nb = {}
        for shift in cands:
            for (prev_shift, changes), prev_cost in dp.items():
                next_changes = changes + (1 if shift != prev_shift else 0)
                if next_changes > p.max_changes:
                    continue
                cost = prev_cost + local_costs[w][shift]
                if shift != prev_shift:
                    cost += 2.2 + 0.2 * abs(shift - prev_shift)
                key = (shift, next_changes)
                if key not in ndp or cost < ndp[key]:
                    ndp[key] = cost
                    nb[key] = (prev_shift, changes)
        if not ndp:
            ndp = {(base_shift, 0): min(dp.values())}
            nb = {(base_shift, 0): min(dp, key=lambda k: dp[k])}
        dp = ndp
        back.append(nb)

    state = min(dp, key=lambda k: dp[k])
    shifts = [base_shift] * cnt
    for w in range(cnt - 1, -1, -1):
        shifts[w] = state[0]
        prev = back[w].get(state)
        if prev is None:
            break
        state = prev
    changes = sum(1 for i in range(1, len(shifts)) if shifts[i] != shifts[i - 1])
    return shifts, win_ticks, changes


def annotate_mapped_notes(
    notes: List[dict], mapped_notes: List[dict], top_ids: Set[int], melody_track: int
) -> List[dict]:
    out = []
    for idx, (src, mapped) in enumerate(zip(notes, mapped_notes)):
        row = dict(mapped)
        row["src_idx"] = idx
        row["src_note"] = src["note"]
        row["is_top"] = idx in top_ids
        row["is_melody_track"] = src["track"] == melody_track
        out.append(row)
    return out


def score_lead_note(
    note: dict, prev_pitch: Optional[int], prev_end: int, step: int, melody_track: int
) -> float:
    score = 0.0
    if note["track"] == melody_track:
        score += 6.0
    if note["is_top"]:
        score += 2.2
    score += min(1.8, 0.35 * note["dur_steps"])
    score += min(1.2, note["vel"] / 96.0)
    if step % 4 == 0:
        score += 0.35
    if note["pitch"] >= 60:
        score += 0.15
    else:
        score -= min(1.5, (60 - note["pitch"]) * 0.08)

    if prev_pitch is not None:
        leap = abs(note["pitch"] - prev_pitch)
        if leap <= 2:
            score += 0.9
        elif leap <= 5:
            score += 0.7
        elif leap <= 9:
            score += 0.2
        elif leap >= 17:
            score -= 2.0
        elif leap >= 12:
            score -= 1.0
        if step < prev_end and note["track"] != melody_track:
            score -= 0.8
        if note["pitch"] == prev_pitch and step <= prev_end:
            score -= 0.4
    return score


def pick_lead_candidate(
    candidates: List[dict], prev_pitch: Optional[int], prev_end: int, step: int, melody_track: int
) -> Optional[dict]:
    melody_candidates = [n for n in candidates if n["track"] == melody_track]
    if melody_candidates:
        pool = melody_candidates
    else:
        if step < prev_end:
            return None
        pool = [n for n in candidates if n["is_top"] or n["dur_steps"] >= 2 or n["vel"] >= 80]
        if not pool:
            return None
        if step % 4 != 0 and max(n["dur_steps"] for n in pool) <= 1:
            return None

    scored = []
    for n in pool:
        scored.append((score_lead_note(n, prev_pitch, prev_end, step, melody_track), n))
    scored.sort(
        key=lambda x: (
            x[0],
            x[1]["track"] == melody_track,
            x[1]["is_top"],
            x[1]["dur_steps"],
            x[1]["pitch"],
        ),
        reverse=True,
    )
    return scored[0][1]


def extract_melody_intervals(mapped_notes: List[dict], melody_track: int) -> Tuple[List[Tuple[int, int, int]], Set[int], dict]:
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)

    lead: List[Tuple[int, int, int, int]] = []
    selected_ids: Set[int] = set()
    stats = {
        "lead_notes": 0,
        "lead_from_melody_track": 0,
        "lead_from_top_note": 0,
        "fallback_lead_notes": 0,
    }

    prev_pitch: Optional[int] = None
    prev_end = -1
    for step in sorted(by_start):
        cand = pick_lead_candidate(by_start[step], prev_pitch, prev_end, step, melody_track)
        if cand is None:
            continue

        start = step
        end = max(start + 1, cand["end_step"])
        if lead:
            last_start, last_end, last_pitch, last_idx = lead[-1]
            if start < last_end:
                if start <= last_start:
                    lead.pop()
                else:
                    lead[-1] = (last_start, start, last_pitch, last_idx)

        if lead and lead[-1][2] == cand["pitch"] and start <= lead[-1][1] + 1:
            last_start, last_end, last_pitch, last_idx = lead[-1]
            lead[-1] = (last_start, max(last_end, end), last_pitch, last_idx)
        else:
            lead.append((start, end, cand["pitch"], cand["src_idx"]))

        selected_ids.add(cand["src_idx"])
        stats["lead_notes"] += 1
        if cand["track"] == melody_track:
            stats["lead_from_melody_track"] += 1
        else:
            stats["fallback_lead_notes"] += 1
        if cand["is_top"]:
            stats["lead_from_top_note"] += 1

        prev_pitch = cand["pitch"]
        prev_end = end

    intervals = [(s, e, p) for s, e, p, _ in lead if e > s]
    return base.merge_intervals_strict(intervals), selected_ids, stats


def build_active_pitch_map(intervals: List[Tuple[int, int, int]], total_steps: int) -> List[Optional[int]]:
    active: List[Optional[int]] = [None] * total_steps
    for start, end, pitch in intervals:
        for step in range(max(0, start), min(total_steps, end)):
            active[step] = pitch
    return active


def assign_support_voices(
    mapped_notes: List[dict],
    lead_ids: Set[int],
    lead_pitch_by_step: List[Optional[int]],
    melody_track: int,
    bass_track: int,
) -> Tuple[Dict[str, List[Tuple[int, int, int]]], int]:
    by_start = defaultdict(list)
    for n in mapped_notes:
        if n["src_idx"] in lead_ids:
            continue
        by_start[n["start_step"]].append(n)

    voices = {"B": [], "C": []}
    pruned = 0

    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda x: (x["pitch"], x["track"]))
        strong = (step % 4) == 0
        eighth = (step % 2) == 0
        dense = len(arr) >= 5
        lead_pitch = lead_pitch_by_step[step] if step < len(lead_pitch_by_step) else None

        filtered = []
        for n in arr:
            if n["dur_steps"] <= 1 and not strong and n["vel"] < 72 and n["track"] != melody_track:
                pruned += 1
                continue
            if dense and not eighth and n["dur_steps"] <= 1 and not n["is_top"] and n["track"] != melody_track:
                pruned += 1
                continue
            if lead_pitch is not None and n["track"] != bass_track and abs(n["pitch"] - lead_pitch) <= 1:
                pruned += 1
                continue
            filtered.append(n)
        if not filtered:
            continue

        used: Set[int] = set()
        bass_candidates = [
            i for i, n in enumerate(filtered) if n["track"] == bass_track or n["pitch"] <= 57
        ]
        if not bass_candidates:
            bass_candidates = [0]
        keep_bass = strong or eighth or len(filtered) <= 2
        keep_bass = keep_bass or any(filtered[i]["dur_steps"] >= 4 for i in bass_candidates)
        if bass_candidates and keep_bass:
            idx = bass_candidates[0]
            bass_note = filtered[idx]
            voices["C"].append((step, bass_note["end_step"], bass_note["pitch"]))
            used.add(idx)

        remaining = [(i, n) for i, n in enumerate(filtered) if i not in used]
        if not remaining:
            continue

        if strong:
            keep = 2 if len(remaining) >= 3 else 1
        elif eighth and not dense:
            keep = 1
        elif len(remaining) == 1 and remaining[0][1]["dur_steps"] >= 4:
            keep = 1
        else:
            keep = 0
        if keep <= 0:
            continue

        scored = []
        for idx, n in remaining:
            score = 0.0
            if n["track"] == melody_track:
                score += 1.1
            if n["is_top"]:
                score += 0.3
            score += min(0.8, 0.2 * n["dur_steps"])
            if lead_pitch is not None:
                delta = lead_pitch - n["pitch"]
                if 2 <= delta <= 12:
                    score += 1.4 - (delta / 14.0)
                elif delta > 12:
                    score += 0.4
                else:
                    score -= 0.8
            else:
                score += 0.01 * n["pitch"]
            if n["pitch"] < 52:
                score -= 0.6
            scored.append((score, idx, n))

        scored.sort(key=lambda x: (-x[0], x[2]["pitch"], x[2]["end_step"]))
        for _, idx, note in scored[:keep]:
            voices["B"].append((step, note["end_step"], note["pitch"]))

    return voices, pruned


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(
        re.escape(safe_base) + r"_analysis_literal_melodylock_v(\d+)\.md$",
        re.I,
    )
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_literal_melodylock_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str], extra: dict) -> None:
    lead_total = max(1, extra["lead_stats"]["lead_notes"])
    lead_track_ratio = extra["lead_stats"]["lead_from_melody_track"] / lead_total * 100.0
    lead_top_ratio = extra["lead_stats"]["lead_from_top_note"] / lead_total * 100.0
    lines = [
        f"# Analysis (Literal MelodyLock Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## MelodyLock Intent",
        "- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line",
        "- avoid turning sustained melody into stacked lead chords",
        "- keep support notes in B/C instead of letting A absorb the whole piano texture",
        "",
        "## Extraction Summary",
        f"- base_shift: {extra['base_shift']}",
        f"- dynamic_windows: {extra['summary']}",
        f"- lead_notes: {extra['lead_stats']['lead_notes']}",
        f"- lead_from_melody_track: {extra['lead_stats']['lead_from_melody_track']} ({lead_track_ratio:.1f}%)",
        f"- lead_from_top_note: {extra['lead_stats']['lead_from_top_note']} ({lead_top_ratio:.1f}%)",
        f"- fallback_lead_notes: {extra['lead_stats']['fallback_lead_notes']}",
        f"- support_notes_pruned: {extra['support_pruned']}",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def convert_midi(input_midi: str, out_dir: str, profile_name: str) -> dict:
    p = PROFILES[profile_name]
    parsed = core.parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)

    base_shift = choose_base_shift_profile(notes, top_ids, parsed["melody_track"], tpb, p)
    shifts, win_ticks, changes = choose_dynamic_shifts_profile(
        notes, top_ids, parsed["melody_track"], tpb, base_shift, p
    )
    tick_per_step = tpb / 4.0
    mapped, dist = core.map_notes(notes, shifts, win_ticks, tick_per_step)
    mapped = annotate_mapped_notes(notes, mapped, top_ids, parsed["melody_track"])

    lead_intervals, lead_ids, lead_stats = extract_melody_intervals(mapped, parsed["melody_track"])
    total_steps = max(n["end_step"] for n in mapped) + 1
    lead_pitch_by_step = build_active_pitch_map(lead_intervals, total_steps)

    support_voices, support_pruned = assign_support_voices(
        mapped, lead_ids, lead_pitch_by_step, parsed["melody_track"], parsed["bass_track"]
    )

    merged = {
        "A": base.merge_intervals_strict(lead_intervals),
        "B": base.merge_intervals_strict(support_voices["B"]),
        "C": base.merge_intervals_strict(support_voices["C"]),
    }

    seg_a = base.intervals_to_segments_limited(merged["A"], total_steps, 1)
    seg_b = base.intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = base.intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)

    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)

    midi_base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = base.next_script_output_path(out_dir, midi_base, "script_literal_melodylock")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    text = "\n".join(
        [
            f"Title: {midi_base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
            f"Source: {os.path.basename(input_midi)}",
            f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
            f"Info: profile={p.name}, {p.desc}",
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
    )

    issues = core.lint_domiso_text(text)
    if issues:
        raise RuntimeError(" | ".join(issues))
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    play = base.evaluate_txt_playability(out_path)
    return {
        "output": out_path,
        "profile": p.name,
        "notes": len(notes),
        "base_shift": base_shift,
        "changes": changes,
        "summary": summary,
        "dist": round(dist, 2),
        "play": play,
        "lead_stats": lead_stats,
        "support_pruned": support_pruned,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Analyze + profile-select + melody-locked literal DoMiSo conversion workflow."
    )
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
        metrics = analyze_midi(parsed)
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
        metrics = analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, profile)
        print(f"output={res['output']}")
        print(f"profile={res['profile']}")
        if reasons:
            print(f"profile_reasons={'; '.join(reasons)}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        metrics = analyze_midi(parsed)
        profile, reasons = recommend_profile(metrics) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, profile)
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(
            report,
            args.input_midi,
            metrics,
            profile,
            reasons,
            {
                "base_shift": res["base_shift"],
                "summary": res["summary"],
                "lead_stats": res["lead_stats"],
                "support_pruned": res["support_pruned"],
            },
        )
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={profile}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "compare":
        pa = base.evaluate_txt_playability(args.file_a)
        pb = base.evaluate_txt_playability(args.file_b)
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
    largs = legacy.parse_args()
    parsed = core.parse_midi(largs.input_midi)
    metrics = analyze_midi(parsed)
    profile, _ = recommend_profile(metrics) if largs.profile == "auto" else (largs.profile, [])
    res = convert_midi(largs.input_midi, largs.out_dir, profile)
    print(f"output={res['output']}")
    print(f"profile={res['profile']}")
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")


if __name__ == "__main__":
    main()
