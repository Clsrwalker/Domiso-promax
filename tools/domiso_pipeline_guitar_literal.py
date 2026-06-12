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
TOP_CHORD_MIN = 72
ALL_PLAYABLE_NOTES = tuple(sorted(PLAYABLE_NOTES))
SINGLE_NOTE_PLAYABLE = tuple(n for n in ALL_PLAYABLE_NOTES if n < TOP_CHORD_MIN)


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
    a_max_poly: int
    b_max_poly: int
    c_max_poly: int
    top_chord_mode: str  # "avoid" | "pad" | "allow"
    chord_pad_min_gap: int
    chord_pad_min_dur: int
    chord_pad_max_dur: int
    chord_pad_melody_limit: int


PROFILES: Dict[str, Profile] = {
    "guitar_literal_strict": Profile(
        "guitar_literal_strict",
        "guitar literal 1:1 mapping, avoid accidental top-row chord-trigger single notes",
        -12,
        12,
        0.20,
        False,
        (0,),
        0,
        4,
        24,
        4,
        "avoid",
        0,
        0,
        0,
        0,
    ),
    "guitar_literal_dense": Profile(
        "guitar_literal_dense",
        "dense guitar literal mapping with controlled top-row chord pads from bass anchors",
        -12,
        12,
        0.10,
        True,
        (0, -2, -1, 1, 2),
        1,
        4,
        32,
        4,
        "pad",
        12,
        3,
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
    if metrics["max_poly"] >= 7 or metrics["bar_density_p90"] >= 24:
        reasons.append("high polyphony/density -> guitar_literal_dense")
        return "guitar_literal_dense", reasons
    reasons.append("default guitar_literal_strict for maximal one-to-one feel")
    return "guitar_literal_strict", reasons


def use_single_note_zone_only(p: Profile) -> bool:
    return p.top_chord_mode in {"avoid", "pad"}


def fold_and_snap_profile(pitch: int, p: Profile) -> Tuple[int, float]:
    folded = pitch
    fold_count = 0
    while folded < core.PLAYABLE_MIN:
        folded += 12
        fold_count += 1
    while folded > core.PLAYABLE_MAX:
        folded -= 12
        fold_count += 1
    candidates = SINGLE_NOTE_PLAYABLE if use_single_note_zone_only(p) else ALL_PLAYABLE_NOTES
    best = min(candidates, key=lambda n: (abs(n - folded), abs(n - pitch), n))
    dist = abs(best - folded) + 0.35 * fold_count
    if use_single_note_zone_only(p) and folded >= TOP_CHORD_MIN:
        dist += 0.25 * (folded - (TOP_CHORD_MIN - 1))
    return best, dist


def evaluate_shift_cost_profile(
    notes: List[dict], shift: int, top_ids: set, melody_track: int, tpb: int, p: Profile
) -> float:
    total = 0.0
    for i, n in enumerate(notes):
        _, dist = fold_and_snap_profile(n["note"] + shift, p)
        dur = n["end"] - n["start"]
        wt = 1.0
        if i in top_ids:
            wt += 0.8
        if n["track"] == melody_track:
            wt += 0.25
        if dur <= max(1, tpb // 6):
            wt *= 0.7
        total += dist * wt
    return total


def choose_base_shift_profile(notes: List[dict], top_ids: set, melody_track: int, tpb: int, p: Profile) -> int:
    best_s, best_c = 0, float("inf")
    for s in range(p.shift_min, p.shift_max + 1):
        c = evaluate_shift_cost_profile(notes, s, top_ids, melody_track, tpb, p) + p.shift_bias * abs(s)
        if c < best_c:
            best_s, best_c = s, c
    return best_s


def choose_dynamic_shifts_profile(
    notes: List[dict], top_ids: set, melody_track: int, tpb: int, base: int, p: Profile
):
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
                _, dist = fold_and_snap_profile(n["note"] + s, p)
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
                cost = pc + local[w][s] + (2.0 if s != ps else 0.0) + 0.2 * abs(s - ps)
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


def map_notes_profile(
    notes: List[dict], shifts: List[int], window_ticks: int, tick_per_step: float, p: Profile
) -> Tuple[List[dict], float]:
    mapped = []
    total_dist = 0.0
    for n in notes:
        win = min(len(shifts) - 1, max(0, n["start"] // window_ticks))
        shift = shifts[win]
        pitch, dist = fold_and_snap_profile(n["note"] + shift, p)
        start_step = int(round(n["start"] / tick_per_step))
        end_step = int(round(n["end"] / tick_per_step))
        if end_step <= start_step:
            end_step = start_step + 1
        total_dist += dist
        mapped.append(
            {
                "start_step": start_step,
                "end_step": end_step,
                "dur_steps": end_step - start_step,
                "pitch": pitch,
                "track": n["track"],
                "vel": n["vel"],
            }
        )
    return mapped, total_dist


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
        if max_poly > 0 and len(pitches) > max_poly:
            # Keep low/high context in C/A, full mid bed in B via higher caps.
            if max_poly <= 4:
                half = max_poly // 2
                pitches = pitches[:half] + pitches[-(max_poly - half):]
            else:
                pitches = pitches[:max_poly]
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


def merge_intervals_strict(intervals: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    by_pitch = defaultdict(list)
    for s, e, p in intervals:
        if e <= s:
            continue
        by_pitch[p].append((s, e))

    merged = []
    for pitch, spans in by_pitch.items():
        spans.sort()
        cur_s, cur_e = spans[0]
        for s, e in spans[1:]:
            if s <= cur_e:
                cur_e = max(cur_e, e)
            else:
                merged.append((cur_s, cur_e, pitch))
                cur_s, cur_e = s, e
        merged.append((cur_s, cur_e, pitch))
    merged.sort(key=lambda x: (x[0], x[2], x[1]))
    return merged


def assign_voices_literal(mapped_notes: List[dict]):
    by_start = defaultdict(list)
    for n in mapped_notes:
        by_start[n["start_step"]].append(n)

    voices = {"A": [], "B": [], "C": []}
    for step in sorted(by_start):
        arr = sorted(by_start[step], key=lambda x: x["pitch"])
        if len(arr) == 1:
            n = arr[0]
            voices["A"].append((step, n["end_step"], n["pitch"]))
            continue
        if len(arr) == 2:
            lo, hi = arr[0], arr[1]
            voices["C"].append((step, lo["end_step"], lo["pitch"]))
            voices["A"].append((step, hi["end_step"], hi["pitch"]))
            continue

        lo = arr[0]
        hi = arr[-1]
        mids = arr[1:-1]
        voices["C"].append((step, lo["end_step"], lo["pitch"]))
        voices["A"].append((step, hi["end_step"], hi["pitch"]))
        for m in mids:
            voices["B"].append((step, m["end_step"], m["pitch"]))

    return voices, 0


def degree_from_pitch(pitch: int) -> int | None:
    degree = core.DEGREE_BY_PC.get(pitch % 12)
    return int(degree) if degree is not None else None


def choose_chord_degree(bass_deg: int, next_deg: int | None) -> int:
    if bass_deg == 7:
        return 7 if next_deg == 1 else 5
    return bass_deg


def attack_set(intervals: List[Tuple[int, int, int]]) -> set:
    return {s for s, _, _ in intervals}


def count_attacks_near(attacks: set, step: int, radius: int = 3) -> int:
    if not attacks:
        return 0
    cnt = 0
    for t in range(step - radius, step + radius + 1):
        if t in attacks:
            cnt += 1
    return cnt


def build_chord_pads_from_bass(
    bass_intervals: List[Tuple[int, int, int]],
    melody_intervals: List[Tuple[int, int, int]],
    p: Profile,
) -> List[Tuple[int, int, int]]:
    if p.top_chord_mode != "pad" or p.chord_pad_min_gap <= 0:
        return []

    mel_attacks = attack_set(melody_intervals)
    entries: List[Tuple[int, int, int]] = []
    for s, e, pitch in sorted(bass_intervals, key=lambda x: (x[0], x[2], x[1])):
        deg = degree_from_pitch(pitch)
        if deg is None or e <= s:
            continue
        entries.append((s, e, deg))

    pads: List[Tuple[int, int, int]] = []
    last_pad = -10**9
    for i, (s, e, deg) in enumerate(entries):
        if (s - last_pad) < p.chord_pad_min_gap:
            continue
        if count_attacks_near(mel_attacks, s, radius=3) > p.chord_pad_melody_limit:
            continue

        next_deg = entries[i + 1][2] if i + 1 < len(entries) else None
        chord_deg = choose_chord_degree(deg, next_deg)
        chord_pitch = TOP_CHORD_MIN + BASE_OFFSETS[chord_deg]
        if chord_pitch not in PLAYABLE_NOTES:
            continue

        span = e - s
        dur = max(p.chord_pad_min_dur, min(p.chord_pad_max_dur, max(2, span // 2)))
        end = min(e, s + dur)
        if end <= s:
            continue
        if pads and pads[-1][2] == chord_pitch and (s - pads[-1][0]) < (p.chord_pad_min_gap * 2):
            continue
        pads.append((s, end, chord_pitch))
        last_pad = s

    return pads


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


def evaluate_top_chord_usage(path: str):
    text = open(path, "r", encoding="utf-8").read()
    base = 60
    for m in re.finditer(r"(?mi)\b1=([A-G]\d?\d?[#b]?)\b", text):
        maybe = key_to_midi(m.group(1))
        if maybe is not None:
            base = maybe
    total = top = safe = 0
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
        if tune >= TOP_CHORD_MIN:
            top += 1
        else:
            safe += 1
    return {
        "notes": total,
        "top_chord_zone": top,
        "safe_single_zone": safe,
    }


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
    mapped, dist = map_notes_profile(notes, shifts, win_ticks, tick_per_step, p)

    voices, removed = assign_voices_literal(mapped)
    chord_pads = build_chord_pads_from_bass(voices["C"], voices["A"], p)
    if chord_pads:
        voices["B"].extend(chord_pads)
    merged = {k: merge_intervals_strict(v) for k, v in voices.items()}
    total_steps = max(n["end_step"] for n in mapped) + 1

    seg_a = intervals_to_segments_limited(merged["A"], total_steps, p.a_max_poly)
    seg_b = intervals_to_segments_limited(merged["B"], total_steps, p.b_max_poly)
    seg_c = intervals_to_segments_limited(merged["C"], total_steps, p.c_max_poly)

    tempo_steps = core.build_tempo_steps(tempos, tick_per_step)
    lines_a = core.serialize_voice(seg_a, tempo_steps)
    lines_b = core.serialize_voice(seg_b, tempo_steps)
    lines_c = core.serialize_voice(seg_c, tempo_steps)

    base = os.path.splitext(os.path.basename(input_midi))[0]
    out_path = next_script_output_path(out_dir, base, "script_guitar_literal")
    summary = core.summarize_windows(shifts)
    dur = core.tick_to_seconds(parsed["max_tick"], tempos, tpb)
    out = [
        f"Title: {base.replace('-', ' ').replace('_', ' ').title()} (auto {p.name})",
        f"Source: {os.path.basename(input_midi)}",
        f"Info: tempo {tempos[0][1]}, duration~{dur:.1f}s, grid 1/16",
        f"Info: profile={p.name}, {p.desc}",
        f"Info: top_chord_mode={p.top_chord_mode} (top row reserved for guitar chords)",
        f"Info: chord_pads_from_bass={len(chord_pads)}",
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
    top_usage = evaluate_top_chord_usage(out_path)
    return {
        "output": out_path,
        "profile": p.name,
        "notes": len(notes),
        "base_shift": base_shift,
        "changes": changes,
        "summary": summary,
        "dist": round(dist, 2),
        "removed": removed,
        "chord_pads": len(chord_pads),
        "top_usage": top_usage,
        "play": play,
    }


def next_report_path(report_dir: str, midi_base: str) -> str:
    safe_base = core.normalize_output_base(midi_base)
    song_dir = os.path.join(report_dir, safe_base)
    os.makedirs(song_dir, exist_ok=True)
    pat = re.compile(re.escape(safe_base) + r"_analysis_guitar_literal_v(\d+)\.md$", re.I)
    mx = 0
    for fn in os.listdir(song_dir):
        m = pat.match(fn)
        if m:
            mx = max(mx, int(m.group(1)))
    return os.path.join(song_dir, f"{safe_base}_analysis_guitar_literal_v{mx + 1}.md")


def write_report(path: str, input_midi: str, metrics: dict, profile: str, reasons: List[str], conv: dict | None = None):
    extra = []
    if conv:
        extra = [
            f"- top chord-zone usage: {conv['top_usage']['top_chord_zone']}/{conv['top_usage']['notes']} "
            f"(safe single-zone {conv['top_usage']['safe_single_zone']}/{conv['top_usage']['notes']})",
            f"- chord pads injected: {conv['chord_pads']}",
            "",
        ]
    lines = [
        f"# Analysis (Guitar Literal Script): {os.path.basename(input_midi)}",
        "",
        "## Metrics",
        *[f"- {k}: {v}" for k, v in metrics.items()],
        "",
        "## Conversion Snapshot",
        *extra,
        "",
        "## Recommended Profile",
        f"- {profile}",
        *[f"- reason: {r}" for r in reasons],
        "",
        "## Guitar Literal Intent",
        "- preserve source note density and rhythm as much as possible",
        "- keep top row for chord triggers; avoid treating it as normal single-note row",
        "- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="Analyze + profile-select + guitar-literal DoMiSo conversion workflow.")
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
        print(f"chord_pads={res['chord_pads']}")
        print(
            f"top_chord_zone_usage={res['top_usage']['top_chord_zone']}/{res['top_usage']['notes']} "
            f"(safe {res['top_usage']['safe_single_zone']}/{res['top_usage']['notes']})"
        )
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "pipeline":
        parsed = core.parse_midi(args.input_midi)
        m = analyze_midi(parsed)
        p, r = recommend_profile(m) if args.profile == "auto" else (args.profile, [])
        res = convert_midi(args.input_midi, args.out_dir, p)
        midi_base = os.path.splitext(os.path.basename(args.input_midi))[0]
        report = next_report_path(args.report_dir, midi_base)
        write_report(report, args.input_midi, m, p, r, conv=res)
        print(f"output={res['output']}")
        print(f"analysis_report={report}")
        print(f"profile={p}")
        print(f"chord_pads={res['chord_pads']}")
        print(
            f"top_chord_zone_usage={res['top_usage']['top_chord_zone']}/{res['top_usage']['notes']} "
            f"(safe {res['top_usage']['safe_single_zone']}/{res['top_usage']['notes']})"
        )
        print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")
        return

    if args.cmd == "compare":
        pa = evaluate_txt_playability(args.file_a)
        pb = evaluate_txt_playability(args.file_b)
        print(json.dumps({"A": {"path": args.file_a, "playability": pa}, "B": {"path": args.file_b, "playability": pb}}, ensure_ascii=False, indent=2))
        return

    legacy = argparse.ArgumentParser(description="legacy guitar-literal convert")
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
    print(f"chord_pads={res['chord_pads']}")
    print(
        f"top_chord_zone_usage={res['top_usage']['top_chord_zone']}/{res['top_usage']['notes']} "
        f"(safe {res['top_usage']['safe_single_zone']}/{res['top_usage']['notes']})"
    )
    print(f"playability={res['play']['playable']}/{res['play']['notes']} ({res['play']['ratio']:.2f}%)")


if __name__ == "__main__":
    main()
