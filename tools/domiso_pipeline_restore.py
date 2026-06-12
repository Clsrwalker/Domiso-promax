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
    melody_mode: str  # "contour" or "top"
    a_harmony: bool
    b_keep_strong: int
    b_keep_normal: int
    c_dense_offbeat: bool
    short_nonmel_steps: int
    short_nonmel_vel: int
    a_max_poly: int
    b_max_poly: int
    c_max_poly: int


PROFILES: Dict[str, Profile] = {
    "restore_strict": Profile(
        "restore_strict",
        "maximum source-faithful restore: mono melody + anchored bass + very light harmony",
        -6,
        6,
        1.9,
        True,
        (0, -1, 1),
        1,
        "contour",
        False,
        1,
        0,
        False,
        2,
        82,
        1,
        1,
        1,
    ),
    "restore_balanced": Profile(
        "restore_balanced",
        "source-faithful restore with moderate support and low ornament pressure",
        -8,
        8,
        1.5,
        True,
        (0, -2, -1, 1, 2),
        2,
        "contour",
        False,
        1,
        1,
        False,
        1,
        76,
        1,
        1,
        1,
    ),
    "restore_dense": Profile(
        "restore_dense",
        "dense-source restore: melody clarity first, compact harmony bed",
        -8,
        8,
        1.2,
        True,
        (0, -2, -1, 1, 2, 3),
        2,
        "contour",
        False,
        2,
        1,
        False,
        1,
        72,
        1,
        1,
        1,
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
    reasons = []
    if (
        metrics["tempo0"] <= 95
        and metrics["tracks"] <= 2
        and (metrics["max_poly"] >= 5 or metrics["bar_density_p90"] >= 18)
    ):
        reasons.append("slow two-track rolled-chord texture -> strict melody/bass restore")
        return "restore_strict", reasons
    if metrics["note_count"] > 1600 or metrics["max_poly"] >= 7 or metrics["bar_density_p90"] >= 26:
        reasons.append("very high density/polyphony -> dense restore with anti-mud caps")
        return "restore_dense", reasons
    reasons.append("default restore-balanced profile")
    return "restore_balanced", reasons


def choose_base_shift_profile(notes: List[dict], top_ids: set, melody_track: int, tpb: int, p: Profile) -> int:
    best_s, best_c = 0, float("inf")
    for s in range(p.shift_min, p.shift_max + 1):
        c = core.evaluate_shift_cost(notes, s, top_ids, melody_track, tpb) + p.shift_bias * abs(s)
        if c < best_c:
            best_s, best_c = s, c
    return best_s


def choose_dynamic_shifts_profile(notes: List[dict], top_ids: set, melody_track: int, tpb: int, base: int, p: Profile):
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
                cost = pc + local[w][s] + (2.5 if s != ps else 0.0) + 0.3 * abs(s - ps)
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
        if max_poly <= 0:
            pitches = []
        elif len(pitches) > max_poly:
            pitches = pitches[-max_poly:]

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


def assign_voices_profile(mapped_notes: List[dict], melody_track: int, bass_track: int, p: Profile):
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)
    voices = {"A": [], "B": [], "C": []}
    prev_a = None
    prev_c = None
    last_c_step = -10_000
    removed = 0

    def choose_melody_idx(arr: List[dict], mel_ids: List[int], prev_pitch: int | None):
        if not mel_ids:
            return None
        if prev_pitch is None:
            return max(
                mel_ids,
                key=lambda i: (arr[i]["dur_steps"], arr[i]["vel"], arr[i]["pitch"]),
            )
        return min(
            mel_ids,
            key=lambda i: (
                abs(arr[i]["pitch"] - prev_pitch),
                -arr[i]["dur_steps"],
                -arr[i]["vel"],
                -arr[i]["pitch"],
            ),
        )

    for step in sorted(by_start):
        arr = sorted(
            by_start[step],
            key=lambda x: (x["pitch"], -x["dur_steps"], -x["vel"], x["track"]),
        )
        filt = []
        for n in arr:
            if (
                n["track"] != melody_track
                and n["dur_steps"] <= p.short_nonmel_steps
                and ((step % 2 == 1) or (n["vel"] < p.short_nonmel_vel))
            ):
                removed += 1
                continue
            filt.append(n)
        if not filt:
            continue

        used = set()
        strong = (step % 4) == 0
        eighth = (step % 2) == 0

        # Voice A: strict single-line melody from melody track only.
        mel_ids = [i for i, n in enumerate(filt) if n["track"] == melody_track]
        a_idx = choose_melody_idx(filt, mel_ids, prev_a)
        if a_idx is not None:
            a = filt[a_idx]
            a_end = max(a["end_step"], step + 2)
            voices["A"].append((step, a_end, a["pitch"]))
            used.add(a_idx)
            prev_a = a["pitch"]

        # Voice C: rooted bass anchor from bass track, mostly on strong/eighth beats.
        bass_ids = [i for i, n in enumerate(filt) if i not in used and n["track"] == bass_track]
        if not bass_ids:
            bass_ids = [i for i, n in enumerate(filt) if i not in used and n["pitch"] <= 60]
        if bass_ids:
            c_idx = min(bass_ids, key=lambda i: (filt[i]["pitch"], -filt[i]["dur_steps"]))
            c = filt[c_idx]
            c_changed = prev_c is None or abs(c["pitch"] - prev_c) >= 2
            keep_c = (
                strong
                or (eighth and c_changed)
                or c["dur_steps"] >= 6
                or (step - last_c_step) >= 8
            )
            if keep_c:
                c_end = max(c["end_step"], step + (4 if strong else 2))
                voices["C"].append((step, c_end, c["pitch"]))
                used.add(c_idx)
                prev_c = c["pitch"]
                last_c_step = step

        # Voice B: very light beat-anchored harmonic color from remaining notes.
        rem = [(i, n) for i, n in enumerate(filt) if i not in used]
        keep_b = p.b_keep_strong if strong else (p.b_keep_normal if eighth else 0)
        if keep_b > 0 and rem:
            rem = [pair for pair in rem if pair[1]["dur_steps"] >= 2]
            if rem:
                target = prev_a - 7 if prev_a is not None else 64
                rem_sorted = sorted(
                    rem,
                    key=lambda pair: (
                        abs(pair[1]["pitch"] - target),
                        -pair[1]["dur_steps"],
                        -pair[1]["vel"],
                    ),
                )
                for i in range(min(keep_b, len(rem_sorted))):
                    _, b = rem_sorted[i]
                    b_end = max(b["end_step"], step + (3 if strong else 2))
                    voices["B"].append((step, b_end, b["pitch"]))

    return voices, removed


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


def convert_midi(input_midi: str, out_dir: str, profile_name: str):
    p = PROFILES[profile_name]
    parsed = core.parse_midi(input_midi)
    tpb = parsed["tpb"]
    notes = parsed["notes"]
    tempos = core.clean_tempos(parsed["tempos"], tpb)
    top_ids = core.build_top_ids(notes)
    base_shift = choose_base_shift_profile(notes, top_ids, parsed["melody_track"], tpb, p)
    shifts, win_ticks, changes = choose_dynamic_shifts_profile(notes, top_ids, parsed["melody_track"], tpb, base_shift, p)
    tick_per_step = tpb / 4.0
    mapped, dist = core.map_notes(notes, shifts, win_ticks, tick_per_step)
    voices, removed = assign_voices_profile(mapped, parsed["melody_track"], parsed["bass_track"], p)
    merged = {k: core.merge_intervals(v) for k, v in voices.items()}
    total_steps = max(n["end_step"] for n in mapped) + 1
    seg_a = intervals_to_segments_limited(merged["A"], total_steps, p.a_max_poly)
    seg_b = intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)
    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)
    base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = next_script_output_path(out_dir, base, "script_restore")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    out = [
        f"Title: {base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
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
        "play": play,
    }


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(re.escape(safe_base) + r"_analysis_restore_v(\d+)\.md$", re.I)
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_restore_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str]):
    lines = [
        f"# Analysis (Restore Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Restore Script Intent",
        "- keep melody line source-faithful and mostly monophonic",
        "- preserve bass root movement and downplay non-source ornament feel",
        "- inject only light strong-beat harmony to avoid clutter",
        "- maintain 21-key playability and parser-safe syntax",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="Analyze + profile-select + convert DoMiSo workflow.")
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
        m = analyze_midi(parsed)
        p, r = recommend_profile(m)
        out = {"input": args.input_midi, "recommended_profile": p, "reasons": r, "metrics": m}
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else out)
        return
    if args.cmd == "convert":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, p)
        print(f"output={res['output']}")
        print(f"profile={res['profile']}")
        if r:
            print(f"profile_reasons={'; '.join(r)}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return
    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, p)
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(report, args.input_midi, m, p, r)
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={p}")
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return
    if args.cmd == "compare":
        pa = evaluate_txt_playability(args.file_a)
        pb = evaluate_txt_playability(args.file_b)
        print(json.dumps({"A": {"path": args.file_a, "playability": pa}, "B": {"path": args.file_b, "playability": pb}}, ensure_ascii=False, indent=2))
        return

    # legacy shortcut
    legacy = argparse.ArgumentParser(description="legacy convert")
    legacy.add_argument("input_midi")
    legacy.add_argument("--out-dir", default=r"d:\domiso\txt")
    legacy.add_argument("--profile", default="auto", choices=["auto"] + sorted(PROFILES))
    l = legacy.parse_args()
    parsed = core.parse_midi(l.input_midi)
    m = analyze_midi(parsed)
    p, _ = recommend_profile(m) if l.profile == "auto" else (l.profile, [])
    res = convert_midi(l.input_midi, l.out_dir, p)
    print(f"output={res['output']}")
    print(f"profile={res['profile']}")
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")


if __name__ == "__main__":
    main()
