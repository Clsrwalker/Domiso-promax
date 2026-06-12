from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple

from .keymaps import map_midi_to_key
from .playback import PlaybackProfile
from .project import normalize_project


@dataclass
class MidiNote:
    start_tick: int
    end_tick: int
    midi_note: int
    velocity: int
    track_index: int
    channel: int


@dataclass
class MidiTrackData:
    index: int
    name: str = ""
    notes: List[MidiNote] = field(default_factory=list)


@dataclass
class MidiFileData:
    ticks_per_beat: int
    tempos: List[Tuple[int, int]]
    tracks: List[MidiTrackData]
    max_tick: int


def _u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], "big")


def _u32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 4], "big")


def _read_varlen(data: bytes, offset: int) -> Tuple[int, int]:
    value = 0
    for _ in range(4):
        if offset >= len(data):
            raise ValueError("truncated MIDI variable-length value")
        byte = data[offset]
        offset += 1
        value = (value << 7) | (byte & 0x7F)
        if byte < 0x80:
            return value, offset
    raise ValueError("invalid MIDI variable-length value")


def _message_data_len(status: int) -> int:
    high = status & 0xF0
    if high in {0xC0, 0xD0}:
        return 1
    if high in {0x80, 0x90, 0xA0, 0xB0, 0xE0}:
        return 2
    raise ValueError(f"unsupported MIDI status 0x{status:02x}")


def _tempo_at_tick(tempos: List[Tuple[int, int]], tick: int) -> int:
    active = tempos[0][1] if tempos else 500000
    for tempo_tick, tempo in tempos:
        if tempo_tick > tick:
            break
        active = tempo
    return active


def _tick_to_ms(tick: int, tempos: List[Tuple[int, int]], ticks_per_beat: int) -> int:
    if tick <= 0:
        return 0
    nodes = sorted(tempos or [(0, 500000)])
    if nodes[0][0] != 0:
        nodes.insert(0, (0, nodes[0][1]))
    total_us = 0.0
    last_tick = 0
    last_tempo = nodes[0][1]
    for tempo_tick, tempo in nodes[1:]:
        if tempo_tick >= tick:
            break
        total_us += (tempo_tick - last_tick) * last_tempo / ticks_per_beat
        last_tick = tempo_tick
        last_tempo = tempo
    total_us += (tick - last_tick) * last_tempo / ticks_per_beat
    return int(round(total_us / 1000.0))


def parse_midi_bytes(data: bytes) -> MidiFileData:
    if len(data) < 14 or data[:4] != b"MThd":
        raise ValueError("not a Standard MIDI file")
    header_len = _u32(data, 4)
    if header_len < 6 or len(data) < 8 + header_len:
        raise ValueError("invalid MIDI header")
    midi_format = _u16(data, 8)
    track_count = _u16(data, 10)
    division = _u16(data, 12)
    if division & 0x8000:
        raise ValueError("SMPTE MIDI timing is not supported")
    if division <= 0:
        raise ValueError("invalid MIDI ticks-per-beat")
    if midi_format not in {0, 1}:
        raise ValueError(f"unsupported MIDI format {midi_format}")

    offset = 8 + header_len
    tempos: List[Tuple[int, int]] = []
    tracks: List[MidiTrackData] = []
    global_max_tick = 0
    for track_index in range(track_count):
        if offset + 8 > len(data) or data[offset : offset + 4] != b"MTrk":
            raise ValueError("missing MIDI track chunk")
        track_len = _u32(data, offset + 4)
        offset += 8
        raw = data[offset : offset + track_len]
        offset += track_len

        track = MidiTrackData(index=track_index, name=f"Track {track_index + 1}")
        abs_tick = 0
        pos = 0
        running_status: int | None = None
        active: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        while pos < len(raw):
            delta, pos = _read_varlen(raw, pos)
            abs_tick += delta
            global_max_tick = max(global_max_tick, abs_tick)
            if pos >= len(raw):
                break
            first = raw[pos]
            if first >= 0x80:
                status = first
                pos += 1
                if 0x80 <= status <= 0xEF:
                    running_status = status
            elif running_status is not None:
                status = running_status
            else:
                raise ValueError("MIDI running status without previous status")

            if status == 0xFF:
                if pos >= len(raw):
                    raise ValueError("truncated MIDI meta event")
                meta_type = raw[pos]
                pos += 1
                length, pos = _read_varlen(raw, pos)
                payload = raw[pos : pos + length]
                pos += length
                if len(payload) != length:
                    raise ValueError("truncated MIDI meta payload")
                if meta_type == 0x2F:
                    break
                if meta_type == 0x03 and payload:
                    track.name = payload.decode("utf-8", errors="replace") or track.name
                elif meta_type == 0x51 and len(payload) == 3:
                    tempos.append((abs_tick, int.from_bytes(payload, "big")))
                continue

            if status in {0xF0, 0xF7}:
                length, pos = _read_varlen(raw, pos)
                pos += length
                continue

            data_len = _message_data_len(status)
            if first < 0x80 and running_status == status:
                msg_data = bytes([first]) + raw[pos + 1 : pos + data_len]
                pos += data_len
            else:
                msg_data = raw[pos : pos + data_len]
                pos += data_len
            if len(msg_data) != data_len:
                raise ValueError("truncated MIDI channel event")

            event_type = status & 0xF0
            channel = status & 0x0F
            if event_type == 0x90 and msg_data[1] > 0:
                active.setdefault((channel, msg_data[0]), []).append((abs_tick, msg_data[1]))
            elif event_type == 0x80 or (event_type == 0x90 and msg_data[1] == 0):
                key = (channel, msg_data[0])
                stack = active.get(key) or []
                if stack:
                    start_tick, velocity = stack.pop()
                    track.notes.append(
                        MidiNote(
                            start_tick=start_tick,
                            end_tick=max(abs_tick, start_tick + 1),
                            midi_note=msg_data[0],
                            velocity=velocity,
                            track_index=track_index,
                            channel=channel,
                        )
                    )
        for (channel, midi_note), stack in active.items():
            for start_tick, velocity in stack:
                track.notes.append(
                    MidiNote(
                        start_tick=start_tick,
                        end_tick=max(abs_tick, start_tick + max(1, division // 2)),
                        midi_note=midi_note,
                        velocity=velocity,
                        track_index=track_index,
                        channel=channel,
                    )
                )
        if track.notes:
            tracks.append(track)

    if not tempos:
        tempos = [(0, 500000)]
    tempos = sorted({tick: tempo for tick, tempo in tempos}.items())
    if tempos[0][0] != 0:
        tempos.insert(0, (0, tempos[0][1]))
    if not tracks:
        raise ValueError("MIDI contains no note events")
    return MidiFileData(ticks_per_beat=division, tempos=tempos, tracks=tracks, max_tick=global_max_tick)


def midi_to_project(
    *,
    data: bytes,
    song_id: str,
    title: str,
    layout: str = "domiso36",
    playback_profile: Dict[str, object] | None = None,
) -> Dict[str, object]:
    parsed = parse_midi_bytes(data)
    project_tracks: List[Dict[str, object]] = []
    for track in parsed.tracks:
        grouped: Dict[Tuple[int, int], List[Dict[str, object]]] = {}
        skipped = 0
        for note in sorted(track.notes, key=lambda n: (n.start_tick, n.midi_note, n.end_tick)):
            key = map_midi_to_key(note.midi_note, layout)
            if key is None:
                skipped += 1
                continue
            start_ms = _tick_to_ms(note.start_tick, parsed.tempos, parsed.ticks_per_beat)
            end_ms = _tick_to_ms(note.end_tick, parsed.tempos, parsed.ticks_per_beat)
            duration_ms = max(1, end_ms - start_ms)
            grouped.setdefault((start_ms, duration_ms), []).append({"key": key, "midi": note.midi_note})
        events = []
        for (time_ms, duration_ms), items in sorted(grouped.items()):
            items.sort(key=lambda item: (int(item["midi"]), str(item["key"])))
            events.append(
                {
                    "timeMs": time_ms,
                    "durationMs": duration_ms,
                    "keys": [str(item["key"]) for item in items],
                    "midiNotes": [int(item["midi"]) for item in items],
                }
            )
        if events:
            project_tracks.append(
                {
                    "id": f"track_{len(project_tracks) + 1}",
                    "name": track.name or f"Track {track.index + 1}",
                    "layout": layout,
                    "events": events,
                    "source": {"format": "midi", "midiTrackIndex": track.index},
                    "stats": {
                        "noteEvents": len(track.notes),
                        "keyEvents": sum(len(event["keys"]) for event in events),
                        "skippedUnmappedNotes": skipped,
                        "durationMs": max((event["timeMs"] + event["durationMs"] for event in events), default=0),
                    },
                }
            )
    if not project_tracks:
        raise ValueError(f"MIDI contains no notes playable on layout {layout}")
    tempo0 = round(60000000 / _tempo_at_tick(parsed.tempos, 0), 2)
    return normalize_project(
        {
            "songId": song_id,
            "title": title,
            "playbackProfile": playback_profile or PlaybackProfile().to_dict(),
            "tracks": project_tracks,
            "meta": {
                "sourceFormat": "midi",
                "ticksPerBeat": parsed.ticks_per_beat,
                "tempoBpm": tempo0,
                "midiTrackCount": len(parsed.tracks),
            },
        }
    )


def midi_base64_to_project(
    *,
    content_base64: str,
    song_id: str,
    title: str,
    layout: str = "domiso36",
    playback_profile: Dict[str, object] | None = None,
) -> Dict[str, object]:
    return midi_to_project(
        data=base64.b64decode(content_base64),
        song_id=song_id,
        title=title,
        layout=layout,
        playback_profile=playback_profile,
    )
