#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "txt" / "image-score-cleanup"
BPM = 80

BASE_OFFSETS = {"1": 0, "2": 2, "3": 4, "4": 5, "5": 7, "6": 9, "7": 11}


SCORE = [
    ("P1", "01", "0 +1 +1 +1 +1 +2 +3 +1", "5 0 0 0 5 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P1", "02", "0 +1 +1 +1 +1 +2 +1 +3", "5 0 0 0 5 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P1", "03", "0 0 0 0 0 0 +1 +2", "5 0 0 0 5 0 0 0", "3 0 0 0 3 0 0 0"),
    ("P1", "04", "+3 +4 +3 +2 0 +3 +2 +1", "6 0 0 0 5 0 0 0", "3 0 0 0 2 0 0 0"),
    ("P1", "05", "0 +1 +1 +1 +1 +2 +3 +1", "4 0 0 0 4 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P1", "06", "0 +1 +1 +1 +7 +1 +7 +6", "5 0 0 0 5 0 0 0", "2 0 0 0 2 0 0 0"),
    ("P1", "07", "0 0 0 0 +3 +5 +2 +1 +7 +5", "6 0 0 0 0 0 0 0", "3 0 0 0 0 0 0 0"),
    ("P1", "08", "3 0 0 +3 +1 +7 +6 +5", "0 0 0 0 0 0 0 0", "0 0 0 0 0 0 0 0"),
    ("P1", "09", "+6 0 +6 0 +6 +5 +3 +5", "4 0 0 0 5 0 0 0", "1 0 0 0 2 0 0 0"),
    ("P1", "10", "0 0 0 +3 +3 +5 +5 +3", "5 0 0 0 5 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P1", "11", "+5 0 +5 +5 +3 +5 +5 +2", "4 0 0 0 5 0 0 0", "1 0 0 0 2 0 0 0"),
    ("P1", "12", "+1 0 0 0 +1 +7 +6 +5", "6 0 0 0 6 0 0 0", "3 0 0 0 3 0 0 0"),
    ("P1", "13", "+6 0 +6 +6 +6 +5 +3 +6", "4 0 0 0 5 0 0 0", "1 0 0 0 2 0 0 0"),
    ("P1", "14", "+5 0 0 0 +3 +4 +5 +1", "5 0 0 0 5 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P1", "15", "0 0 +3 +2 0 0 +1 +1", "4 0 0 0 5 0 0 0", "1 0 0 0 2 0 0 0"),
    ("P1", "16", "0 0 0 0 +1 +7 +6 +5", "6 0 0 0 0 0 0 0", "3 0 0 0 0 0 0 0"),
    ("P2", "16", "+6 0 +6 +5 +6 +1 +2 +3", "4 0 0 0 4 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P2", "17", "+5 0 0 0 +3 +5 +5 +6", "5 0 0 0 4 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P2", "18", "+1 0 0 +6 +1 +2 +3 +5", "4 0 0 0 4 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P2", "19", "+3 0 0 0 +3 +5 +6 +1 +2", "5 0 0 0 5 0 0 0 0", "1 0 0 0 1 0 0 0 0"),
    ("P2", "20", "+3 0 0 0 +2 +4 +3 +2", "4 0 0 0 5 0 0 0", "1 0 0 0 2 0 0 0"),
    ("P2", "21", "+2 0 0 0 +1 +2 0 +3", "5 0 0 0 5 0 0 0", "2 0 0 0 2 0 0 0"),
    ("P2", "22", "+4 0 +3 0 +1 0 0 +7", "6 0 0 0 4 0 0 0", "3 0 0 0 2 0 0 0"),
    ("P2", "23", "+1 0 0 0 0 0 0 0", "5 0 0 0 5 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P2", "24", "0 +1 +1 +1 +1 +2 +3 +1", "5 0 5 0 5 0 0 0", "1 0 1 0 1 0 0 0"),
    ("P2", "25", "0 +1 +1 +1 +1 +2 +1 +3", "5 0 5 0 5 0 0 0", "1 0 1 0 1 0 0 0"),
    ("P2", "26", "0 0 0 0 0 0 +1 +2", "5 0 5 0 5 0 0 0", "3 0 3 0 3 0 0 0"),
    ("P2", "27", "+3 +4 +3 +2 0 +3 +2 +1", "6 0 6 0 5 0 5 0", "3 0 3 0 2 0 2 0"),
    ("P2", "28", "0 +1 +1 +1 +1 +2 +3 +1", "4 0 4 0 4 0 0 0", "1 0 1 0 1 0 0 0"),
    ("P2", "29", "0 +1 +1 +1 +7 +1 +7 +6", "5 0 5 0 5 0 5 0", "2 0 2 0 2 0 2 0"),
    ("P2", "30", "0 0 0 0 0 +6 +1 +2", "6 0 6 0 6 0 0 0", "3 0 3 0 3 0 0 0"),
    ("P2", "31", "+1 0 0 +3 +1 +7 +6 +5", "6 0 0 0 0 0 0 0", "3 0 0 0 0 0 0 0"),
    ("P3", "32", "+6 0 +6 0 +6 +5 +3 +5", "4 0 4 0 5 0 5 0", "1 0 1 0 2 0 2 0"),
    ("P3", "33", "0 0 0 0 +3 +5 +5 +3", "5 0 5 0 5 0 5 0", "1 0 1 0 1 0 1 0"),
    ("P3", "34", "+5 0 +5 +5 +3 +5 +5 +2", "4 0 4 0 5 0 5 0", "1 0 1 0 2 0 2 0"),
    ("P3", "35", "+1 0 0 0 +1 +7 +6 +5", "6 0 6 0 6 0 6 0", "3 0 3 0 3 0 3 0"),
    ("P3", "36", "+6 0 +6 +6 +6 +5 +3 +6", "4 0 4 0 5 0 5 0", "1 0 1 0 2 0 2 0"),
    ("P3", "37", "+5 0 0 0 +3 +4 +5 +1", "5 0 5 0 5 0 5 0", "1 0 1 0 1 0 1 0"),
    ("P3", "38", "0 0 +3 +2 0 0 +1 +1", "4 0 4 0 5 0 0 0", "1 0 1 0 2 0 0 0"),
    ("P3", "39", "0 0 0 +3 +1 +7 +6 +5", "6 0 6 0 6 0 6 0", "3 0 3 0 3 0 3 0"),
    ("P3", "40", "+6 0 +6 0 +6 +5 +3 +5", "4 0 4 0 5 0 5 0", "1 0 1 0 2 0 2 0"),
    ("P3", "41", "0 0 0 0 +3 +5 +5 +3", "5 0 5 0 5 0 5 0", "1 0 1 0 1 0 1 0"),
    ("P3", "42", "+5 0 +5 +5 +3 +5 +5 +2", "4 0 4 0 5 0 5 0", "1 0 1 0 2 0 2 0"),
    ("P3", "43", "0 +1 0 0 +1 +7 +6 +5", "6 0 6 0 6 0 6 0", "3 0 3 0 3 0 3 0"),
    ("P3", "44", "+6 0 +6 +6 +6 +5 +3 +6", "4 0 4 0 5 0 5 0", "1 0 1 0 2 0 2 0"),
    ("P3", "45", "+5 0 0 +1 +3 +4 +5 +1", "5 0 0 0 5 0 0 0", "1 0 0 0 1 0 0 0"),
    ("P3", "46", "0 0 +3 +2 0 0 +1 +1", "4 0 0 0 5 0 0 0", "1 0 0 0 2 0 0 0"),
    ("P3", "47", "0 0 0 0 0 0 0 0", "5 0 0 0 0 0 0 0", "1 0 0 0 0 0 0 0"),
]


def split_notes(row: str) -> list[str]:
    return row.split()


def normalize_bar(melody: str, harmony: str, bass: str) -> tuple[list[str], list[str], list[str]]:
    rows = [split_notes(melody), split_notes(harmony), split_notes(bass)]
    length = max(len(row) for row in rows)
    return tuple(row + ["0"] * (length - len(row)) for row in rows)  # type: ignore[return-value]


def note_pitch(note: str) -> int:
    if note == "0":
        return -999
    m = re.fullmatch(r"([+\-]*)([1-7])", note)
    if not m:
        raise ValueError(f"bad note: {note}")
    prefix, degree = m.groups()
    return 60 + BASE_OFFSETS[degree] + 12 * (prefix.count("+") - prefix.count("-"))


def render_note(note: str) -> str:
    if note == "0":
        return "0/"
    return f"{note}/"


def render_chord(notes: list[str]) -> str:
    active = sorted({note for note in notes if note != "0"}, key=note_pitch)
    if not active:
        return "0/"
    if len(active) == 1:
        return f"{active[0]}/"
    return f"( {' '.join(active)} )/"


def wrap(lines: list[str]) -> list[str]:
    return lines


def next_paths() -> tuple[Path, Path, Path, Path, int]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prefix = "image_score_manual_sky"
    version = 1
    while any((OUT_DIR / f"{prefix}_{kind}_v{version}.txt").exists() for kind in ("duet_A", "duet_B", "full")):
        version += 1
    return (
        OUT_DIR / f"{prefix}_duet_A_v{version}.txt",
        OUT_DIR / f"{prefix}_duet_B_v{version}.txt",
        OUT_DIR / f"{prefix}_full_v{version}.txt",
        OUT_DIR / f"{prefix}_report_v{version}.md",
        version,
    )


def build_lines(kind: str) -> tuple[list[str], dict[str, int]]:
    lines: list[str] = []
    stats = {"slots": 0, "note_events": 0, "chord_events": 0, "bars": len(SCORE)}
    last_page = None
    for page, bar, melody, harmony, bass in SCORE:
        if page != last_page:
            if lines:
                lines.append("")
            lines.append(f"; {page}")
            last_page = page
        m_row, h_row, b_row = normalize_bar(melody, harmony, bass)
        tokens: list[str] = []
        for m, h, b in zip(m_row, h_row, b_row):
            if kind == "A":
                tok = render_note(m)
                if m != "0":
                    stats["note_events"] += 1
            elif kind == "B":
                tok = render_chord([b, h])
                active = [x for x in (b, h) if x != "0"]
                stats["note_events"] += len(set(active))
                if len(set(active)) > 1:
                    stats["chord_events"] += 1
            else:
                tok = render_chord([b, h, m])
                active = [x for x in (b, h, m) if x != "0"]
                stats["note_events"] += len(set(active))
                if len(set(active)) > 1:
                    stats["chord_events"] += 1
            tokens.append(tok)
            stats["slots"] += 1
        lines.append(" ".join(tokens))
    return wrap(lines), stats


def build_text(title: str, part: str, role: str, lines: list[str]) -> str:
    return "\n".join(
        [
            f"Title: {title}",
            "Source: manual numbered score from screenshots",
            f"Info: part={part}, role={role}",
            "Info: each token is one eighth-note slot; / suffix = 0.5 beat",
            "Info: count_in=4 beats; start both computers together for duet A/B",
            "Info: Sky 15-key layout C4-C6",
            "",
            "1=C4",
            f"bpm={BPM}",
            "",
            "; Sync Count-In",
            "0---",
            "",
            f"; Manual {part} {role}",
            f"bpm={BPM}",
            *lines,
            "",
        ]
    )


def validate_text(text: str) -> list[str]:
    issues: list[str] = []
    if re.search(r"(?<![A-Za-z0-9_])[+\-]*[1-7][#b](?![A-Za-z0-9_])", text):
        issues.append("accidentals found")
    for note in re.findall(r"(?<![A-Za-z0-9_])([+\-]*[1-7])(?:[\/\-.]|[\s)])", text):
        pitch = note_pitch(note)
        if pitch < 60 or pitch > 83:
            issues.append(f"out of Sky C4-B5 range: {note}")
    return sorted(set(issues))


def main() -> None:
    out_a, out_b, out_full, report, version = next_paths()
    lines_a, stats_a = build_lines("A")
    lines_b, stats_b = build_lines("B")
    lines_full, stats_full = build_lines("FULL")

    text_a = build_text(f"Image Score Manual Sky Duet A v{version}", "A", "Melody", lines_a)
    text_b = build_text(f"Image Score Manual Sky Duet B v{version}", "B", "Harmony+Bass", lines_b)
    text_full = build_text(f"Image Score Manual Sky Full v{version}", "FULL", "Melody+Harmony+Bass", lines_full)
    issues = {
        "A": validate_text(text_a),
        "B": validate_text(text_b),
        "FULL": validate_text(text_full),
    }
    if any(issues.values()):
        raise SystemExit(f"validation failed: {issues}")

    out_a.write_text(text_a, encoding="utf-8", newline="\n")
    out_b.write_text(text_b, encoding="utf-8", newline="\n")
    out_full.write_text(text_full, encoding="utf-8", newline="\n")
    report.write_text(
        "\n".join(
            [
                f"# Manual Image Score Sky v{version}",
                "",
                f"- bpm: {BPM}",
                "- slot_duration: eighth note (`/` suffix)",
                f"- bars: {len(SCORE)}",
                f"- duet_A: {out_a}",
                f"- duet_B: {out_b}",
                f"- full: {out_full}",
                "",
                "## Stats",
                f"- A: {stats_a}",
                f"- B: {stats_b}",
                f"- FULL: {stats_full}",
                "",
                "## Validation",
                f"- A: {issues['A'] or 'ok'}",
                f"- B: {issues['B'] or 'ok'}",
                f"- FULL: {issues['FULL'] or 'ok'}",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"A={out_a}")
    print(f"B={out_b}")
    print(f"FULL={out_full}")
    print(f"REPORT={report}")


if __name__ == "__main__":
    main()
