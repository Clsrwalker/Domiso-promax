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


PROFILES: Dict[str, Profile] = {
    "piano_solo": Profile(
        "piano_solo", "melody-first, sparse harmony",
        -4, 4, 2.1, False, (0,), 0, "contour", False, 1, 0, False
    ),
    "pop_ballad": Profile(
        "pop_ballad", "balanced 3-layer restore",
        -6, 6, 1.6, True, (0, -2, -1, 1, 3), 2, "contour", False, 1, 1, False
    ),
    "epic_dense": Profile(
        "epic_dense", "higher density, anti-mud filter",
        -8, 8, 1.0, True, (0, -2, -1, 1, 2, 3), 3, "top", True, 2, 1, True
    ),
    "anime_op": Profile(
        "anime_op", "fast melody-forward profile",
        -6, 6, 1.3, True, (0, -1, 1, 2), 2, "contour", True, 1, 1, False
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
    if metrics["note_count"] > 1400 or metrics["max_poly"] >= 6 or metrics["bar_density_p90"] >= 14:
        reasons.append("high density/polyphony")
        return "epic_dense", reasons
    if metrics["tempo0"] >= 145 and metrics["note_count"] >= 650:
        reasons.append("fast and note-rich")
        return "anime_op", reasons
    if metrics["time_sig"] == "3/4" and metrics["tracks"] <= 2:
        reasons.append("3/4 + few tracks -> melody clarity")
        return "piano_solo", reasons
    reasons.append("default balanced")
    return "pop_ballad", reasons


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


def assign_voices_profile(mapped_notes: List[dict], melody_track: int, bass_track: int, p: Profile):
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)
    voices = {"A": [], "B": [], "C": []}
    prev_a = None
    removed = 0
    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda x: (x["pitch"], x["track"]))
        filt = []
        for n in arr:
            if n["dur_steps"] <= 1 and (step % 2 == 1) and n["vel"] < 72 and n["track"] != melody_track:
                removed += 1
                continue
            filt.append(n)
        if not filt:
            continue
        used = set()
        strong = (step % 4) == 0
        dense = len(filt) >= 5
        if p.melody_mode == "contour":
            mel = [i for i, n in enumerate(filt) if n["track"] == melody_track]
            cand = mel if mel else list(range(len(filt)))
            if prev_a is None:
                a_idx = max(cand, key=lambda i: filt[i]["pitch"])
            else:
                a_idx = min(cand, key=lambda i: (abs(filt[i]["pitch"] - prev_a), -filt[i]["pitch"]))
        else:
            a_idx = len(filt) - 1
        a = filt[a_idx]
        voices["A"].append((step, a["end_step"], a["pitch"]))
        used.add(a_idx)
        prev_a = a["pitch"]
        if p.a_harmony and strong and len(filt) >= 4:
            for i in range(len(filt) - 2, -1, -1):
                if i in used:
                    continue
                iv = filt[a_idx]["pitch"] - filt[i]["pitch"]
                if 3 <= iv <= 8:
                    n = filt[i]
                    voices["A"].append((step, n["end_step"], n["pitch"]))
                    used.add(i)
                    break
        cands = [i for i, n in enumerate(filt) if i not in used and (n["track"] == bass_track or n["pitch"] <= 60)]
        if not cands:
            cands = [i for i in range(len(filt)) if i not in used]
        if cands and (p.c_dense_offbeat or not dense or strong or step % 2 == 0):
            i = cands[0]
            n = filt[i]
            voices["C"].append((step, n["end_step"], n["pitch"]))
            used.add(i)
        rem = [(i, n) for i, n in enumerate(filt) if i not in used]
        if rem:
            if dense and not p.c_dense_offbeat and not (strong or step % 2 == 0):
                rem = []
            keep = p.b_keep_strong if strong else p.b_keep_normal
            keep = max(0, min(keep, len(rem)))
            mid = max(0, (len(rem) - keep) // 2)
            for i in range(mid, mid + keep):
                _, n = rem[i]
                voices["B"].append((step, n["end_step"], n["pitch"]))
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
    seg_a = core.intervals_to_segments(merged["A"], total_steps, "A")
    seg_b = core.intervals_to_segments(merged["B"], total_steps, "B")
    seg_c = core.intervals_to_segments(merged["C"], total_steps, "C")
    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)
    base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = core.next_output_path(out_dir, base)
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
    pat = re.compile(re.escape(safe_base) + r"_analysis_v(\d+)\.md$", re.I)
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str]):
    lines = [
        f"# Analysis: {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Manual Arrangement Checklist",
        "- keep melody singable first, avoid forced leap",
        "- ornaments source-derived only",
        "- keep bass harmonic roots at section edges",
        "- check parser syntax and playable ratio after edits",
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
