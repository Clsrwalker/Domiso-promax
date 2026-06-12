from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .keymaps import map_midi_to_key


BASE_OFFSETS = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
ARPEGGIO_DELAY_MS = 40


@dataclass
class ParseDiagnostic:
    line: int
    message: str


@dataclass
class ParsedTokenNote:
    midi_note: Optional[int]
    duration_beats: float
    arpeggio: bool = False


@dataclass
class NoteEvent:
    time_ms: int
    duration_ms: int
    midi_note: int

    @property
    def end_ms(self) -> int:
        return self.time_ms + self.duration_ms


@dataclass
class ParseContext:
    base_midi: int = 60
    beat_ms: float = 750.0
    offset_ms: float = 0.0
    total_beats: float = 0.0
    last_note_duration_ms: int = 0
    arpeggio_accumulated_ms: int = 0
    events: List[NoteEvent] = field(default_factory=list)
    diagnostics: List[ParseDiagnostic] = field(default_factory=list)


def duration_from_marks(base_beats: float, marks: str) -> float:
    if not marks:
        return base_beats
    result = base_beats
    last_base = base_beats
    i = 0
    while i < len(marks):
        mark = marks[i]
        count = 0
        while i < len(marks) and marks[i] == mark:
            count += 1
            i += 1
        if mark == "/":
            nxt = last_base / (2**count)
            result = result - last_base + nxt
            last_base = nxt
        elif mark == "-":
            result += count
            last_base = 1.0
        elif mark == ".":
            dot_base = last_base
            for _ in range(count):
                dot_base /= 2.0
                result += dot_base
            last_base = dot_base
    return max(0.0, result)


def midi_for_key_control(key_text: str, pitch_naming: str = "standard") -> Optional[int]:
    m = re.match(r"^([A-Ga-g])(\d{0,2})([#b]?)$", key_text.strip())
    if not m:
        return None
    name, octave_text, acc = m.groups()
    pc = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name.upper()]
    if acc == "#":
        pc += 1
    elif acc == "b":
        pc -= 1
    if not octave_text:
        return 60 + (pc % 12)
    octave = int(octave_text)
    if pitch_naming == "domiso":
        return octave * 12 + (pc % 12)
    return (octave + 1) * 12 + (pc % 12)


def apply_control_commands(line: str, line_number: int, ctx: ParseContext, pitch_naming: str) -> None:
    bpm_match = re.search(r"(?i)\bbpm\s*=\s*(\d+)", line)
    if bpm_match:
        bpm = int(bpm_match.group(1))
        if 1 <= bpm <= 480:
            ctx.beat_ms = 60000.0 / bpm
        else:
            ctx.beat_ms = 60000.0 / 80.0
            ctx.diagnostics.append(ParseDiagnostic(line_number, f"BPM {bpm} is outside 1..480; reset to 80."))

    key_match = re.search(r"(?i)\b1\s*=\s*([A-G](?:\d{0,2})[#b]?)", line)
    if key_match:
        base = midi_for_key_control(key_match.group(1), pitch_naming)
        if base is not None:
            ctx.base_midi = base
        else:
            ctx.diagnostics.append(ParseDiagnostic(line_number, f"Could not parse key control 1={key_match.group(1)}."))

    rollback_match = re.search(r"(?i)\brollback\s*=\s*(\d+(?:\.\d+)?)", line)
    if rollback_match:
        beats = float(rollback_match.group(1))
        ctx.offset_ms = max(0.0, ctx.offset_ms - beats * ctx.beat_ms)
        ctx.last_note_duration_ms = 0
        ctx.arpeggio_accumulated_ms = 0


def parse_note_token(token: str, line_number: int, ctx: ParseContext) -> Optional[ParsedTokenNote]:
    m = re.match(r"(?i)^(~)?([+-]*)([0-7])([#b])?([/\-.]*)$", token)
    if not m:
        return None
    arpeggio, scale, degree_text, semitone, marks = m.groups()
    degree = int(degree_text)
    duration_beats = duration_from_marks(1.0, marks)
    if degree == 0:
        return ParsedTokenNote(None, duration_beats, bool(arpeggio))
    if degree not in BASE_OFFSETS:
        ctx.diagnostics.append(ParseDiagnostic(line_number, f"Unsupported note degree {degree}."))
        return None
    octave_offset = -len(scale) if scale.startswith("-") else len(scale)
    midi = ctx.base_midi + BASE_OFFSETS[degree] + octave_offset * 12
    if semitone == "#":
        midi += 1
    elif semitone and semitone.lower() == "b":
        midi -= 1
    return ParsedTokenNote(midi, duration_beats, bool(arpeggio))


def append_standalone(note: ParsedTokenNote, ctx: ParseContext) -> None:
    duration_ms_float = note.duration_beats * ctx.beat_ms
    is_arpeggio = False
    if note.arpeggio:
        if ctx.last_note_duration_ms <= 0:
            return
        if duration_ms_float <= ctx.arpeggio_accumulated_ms + 20:
            return
        is_arpeggio = True
        ctx.offset_ms -= ctx.last_note_duration_ms
        ctx.offset_ms += ARPEGGIO_DELAY_MS
        ctx.arpeggio_accumulated_ms += ARPEGGIO_DELAY_MS
        duration_ms_float -= ctx.arpeggio_accumulated_ms
    else:
        ctx.arpeggio_accumulated_ms = 0

    start = max(0, round(ctx.offset_ms))
    duration_ms = max(1, round(duration_ms_float))
    if note.midi_note and note.midi_note > 0:
        ctx.events.append(NoteEvent(start, duration_ms, note.midi_note))
    ctx.offset_ms += duration_ms_float
    if not is_arpeggio:
        ctx.total_beats += note.duration_beats
    ctx.last_note_duration_ms = duration_ms


def close_chord(notes: List[ParsedTokenNote], marks: str, ctx: ParseContext) -> None:
    if not notes:
        return
    base_beats = max(n.duration_beats for n in notes)
    duration_beats = duration_from_marks(base_beats, marks)
    duration_ms = max(1, round(duration_beats * ctx.beat_ms))
    start = max(0, round(ctx.offset_ms))
    for note in notes:
        if note.midi_note and note.midi_note > 0:
            ctx.events.append(NoteEvent(start, duration_ms, note.midi_note))
    ctx.offset_ms += duration_ms
    ctx.total_beats += duration_beats
    ctx.last_note_duration_ms = duration_ms
    ctx.arpeggio_accumulated_ms = 0


def close_multiplet(notes: List[ParsedTokenNote], marks: str, ctx: ParseContext) -> None:
    if not notes:
        return
    total_duration_beats = duration_from_marks(1.0, marks)
    weight = sum(n.duration_beats for n in notes)
    if weight <= 0:
        return
    multiplier = total_duration_beats / weight
    for note in notes:
        note_duration_beats = note.duration_beats * multiplier
        duration_ms = max(1, round(note_duration_beats * ctx.beat_ms))
        start = max(0, round(ctx.offset_ms))
        if note.midi_note and note.midi_note > 0:
            ctx.events.append(NoteEvent(start, duration_ms, note.midi_note))
        ctx.offset_ms += duration_ms
        ctx.last_note_duration_ms = duration_ms
    ctx.total_beats += total_duration_beats
    ctx.arpeggio_accumulated_ms = 0


def parse_domiso_text(text: str, pitch_naming: str = "standard") -> Tuple[List[NoteEvent], List[ParseDiagnostic], int]:
    ctx = ParseContext()
    naming = "domiso" if str(pitch_naming).lower() == "domiso" else "standard"
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    for line_number, line in enumerate(lines, start=1):
        apply_control_commands(line, line_number, ctx, naming)
        group: str | None = None
        chord_cache: List[ParsedTokenNote] = []
        multiplet_cache: List[ParsedTokenNote] = []
        for token in re.split(r"[ \t]+", line.strip()):
            if not token:
                continue
            if token == "(" and group is None:
                group = "chord"
                chord_cache = []
                continue
            if token == "{" and group is None:
                group = "multiplet"
                multiplet_cache = []
                continue
            if token.startswith(")") and group == "chord":
                close_chord(chord_cache, token[1:], ctx)
                group = None
                chord_cache = []
                continue
            if token.startswith("}") and group == "multiplet":
                close_multiplet(multiplet_cache, token[1:], ctx)
                group = None
                multiplet_cache = []
                continue
            note = parse_note_token(token, line_number, ctx)
            if note is None:
                continue
            if group == "chord":
                chord_cache.append(note)
            elif group == "multiplet":
                multiplet_cache.append(note)
            else:
                append_standalone(note, ctx)
    events = sorted(ctx.events, key=lambda e: (e.time_ms, e.midi_note, e.duration_ms))
    total_ms = max([round(ctx.offset_ms), *(e.end_ms for e in events)], default=0)
    return events, ctx.diagnostics, total_ms


def note_events_to_track(
    *,
    track_id: str,
    name: str,
    text: str,
    layout: str,
    pitch_naming: str = "standard",
) -> Dict[str, object]:
    notes, diagnostics, total_ms = parse_domiso_text(text, pitch_naming=pitch_naming)
    grouped: Dict[Tuple[int, int], List[Dict[str, object]]] = {}
    skipped = 0
    for note in notes:
        key = map_midi_to_key(note.midi_note, layout)
        if key is None:
            skipped += 1
            continue
        grouped.setdefault((note.time_ms, note.duration_ms), []).append(
            {"midi": note.midi_note, "key": key}
        )
    events = []
    for (time_ms, duration_ms), items in sorted(grouped.items()):
        items.sort(key=lambda x: (int(x["midi"]), str(x["key"])))
        events.append(
            {
                "timeMs": time_ms,
                "durationMs": duration_ms,
                "keys": [str(i["key"]) for i in items],
                "midiNotes": [int(i["midi"]) for i in items],
            }
        )
    return {
        "id": track_id,
        "name": name or track_id,
        "layout": layout,
        "events": events,
        "source": {"format": "domiso_txt", "pitchNaming": "domiso" if pitch_naming == "domiso" else "standard"},
        "stats": {
            "noteEvents": len(notes),
            "keyEvents": sum(len(ev["keys"]) for ev in events),
            "skippedUnmappedNotes": skipped,
            "durationMs": total_ms,
            "diagnostics": [d.__dict__ for d in diagnostics],
        },
    }
