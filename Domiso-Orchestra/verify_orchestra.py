from __future__ import annotations

import tempfile
from pathlib import Path

from domiso_orchestra.client_config import load_client_config, save_client_config
from domiso_orchestra.domiso_parser import note_events_to_track, parse_domiso_text
from domiso_orchestra.domiso_sheet import decrypt_dms_bytes, encrypt_dms_bytes, split_published_text
from domiso_orchestra.midi_import import midi_to_project, parse_midi_bytes
from domiso_orchestra.playback import (
    DryRunBackend,
    PlaybackAction,
    PlaybackEngine,
    PlaybackProfile,
    build_actions,
    slice_actions_from_position,
)
from domiso_orchestra.project import normalize_project, project_from_domiso_tracks


def _vlq(value: int) -> bytes:
    parts = [value & 0x7F]
    value >>= 7
    while value:
        parts.append(0x80 | (value & 0x7F))
        value >>= 7
    return bytes(reversed(parts))


def _track(events: bytes) -> bytes:
    return b"MTrk" + len(events).to_bytes(4, "big") + events


def _minimal_midi() -> bytes:
    header = b"MThd" + (6).to_bytes(4, "big") + (1).to_bytes(2, "big") + (2).to_bytes(2, "big") + (480).to_bytes(2, "big")
    tempo = b"\x00\xff\x03\x05Tempo\x00\xff\x51\x03\x07\xa1\x20\x00\xff\x2f\x00"
    melody = (
        b"\x00\xff\x03\x06Melody"
        + b"\x00\x90\x3c\x40"
        + _vlq(480)
        + b"\x80\x3c\x00"
        + b"\x00\x90\x40\x40"
        + _vlq(480)
        + b"\x80\x40\x00"
        + b"\x00\xff\x2f\x00"
    )
    return header + _track(tempo) + _track(melody)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        config_path = Path(tmp) / "client.json"
        save_client_config(config_path, {"clientId": "PC-A", "inputDelayOffsetMs": -20})
        config = load_client_config(config_path)
        assert config["clientId"] == "PC-A"
        assert config["inputDelayOffsetMs"] == -20

    pitch_text = """
    bpm=120
    1=C4
    1 0 2# 3b
    """
    notes, diagnostics, total_ms = parse_domiso_text(pitch_text)
    assert not diagnostics, diagnostics
    assert [n.midi_note for n in notes] == [60, 63, 63]
    assert [n.time_ms for n in notes] == [0, 1000, 1500]
    assert total_ms == 2000
    domiso_named, diagnostics, _ = parse_domiso_text("1=C5\n1 2\n", pitch_naming="domiso")
    assert not diagnostics, diagnostics
    assert [n.midi_note for n in domiso_named] == [60, 62]
    domiso_c4, diagnostics, _ = parse_domiso_text("1=C4\n1\n", pitch_naming="domiso")
    assert not diagnostics, diagnostics
    assert [n.midi_note for n in domiso_c4] == [48]

    comment, sheet = split_published_text("Title: Public\n======\nbpm=120\n1 2\n")
    assert comment == "Title: Public"
    assert sheet == "bpm=120\r\n1 2"
    dms_bytes = encrypt_dms_bytes("Title: Public", "bpm=120\n1 2\n")
    dms_comment, dms_sheet = decrypt_dms_bytes(dms_bytes)
    assert dms_comment == "Title: Public"
    assert dms_sheet == "bpm=120\n1 2\n"

    midi = _minimal_midi()
    parsed_midi = parse_midi_bytes(midi)
    assert parsed_midi.ticks_per_beat == 480
    assert len(parsed_midi.tracks) == 1
    midi_project = midi_to_project(data=midi, song_id="midi", title="MIDI", layout="domiso36")
    assert midi_project["tracks"][0]["events"][0]["keys"] == ["a"]
    assert midi_project["tracks"][0]["events"][1]["keys"] == ["d"]

    group_text = """
    bpm=120
    1 2 3 4
    rollback=4
    ( 1 3 5 )--
    """
    notes, diagnostics, total_ms = parse_domiso_text(group_text)
    assert not diagnostics, diagnostics
    assert len(notes) == 7, len(notes)
    time_counts = {time_ms: sum(1 for n in notes if n.time_ms == time_ms) for time_ms in {n.time_ms for n in notes}}
    assert time_counts == {0: 4, 500: 1, 1000: 1, 1500: 1}
    assert total_ms >= 1500

    multiplet_text = """
    bpm=120
    0 5 6 5
    { 1 3 5 +1 }
    """
    notes, diagnostics, total_ms = parse_domiso_text(multiplet_text)
    assert not diagnostics, diagnostics
    assert len(notes) == 7, len(notes)
    assert total_ms >= 2000

    arpeggio_text = """
    bpm=120
    1 ~3 ~5
    """
    notes, diagnostics, total_ms = parse_domiso_text(arpeggio_text)
    assert not diagnostics, diagnostics
    assert [n.time_ms for n in notes] == [0, 40, 80]
    assert total_ms == 500

    track_a = note_events_to_track(track_id="track_1", name="A", text=group_text, layout="sky15")
    track_b = note_events_to_track(track_id="track_2", name="B", text=multiplet_text, layout="sky15")
    domiso36_track = note_events_to_track(track_id="track_3", name="Sharp", text="bpm=120\n1=C4\n1#\n", layout="domiso36")
    assert domiso36_track["events"][0]["keys"] == ["shift+a"]

    converted = project_from_domiso_tracks(
        song_id="converted",
        title="Converted",
        tracks=[
            {"id": "left", "name": "Left", "text": group_text},
            {"id": "right", "name": "Right", "text": multiplet_text},
        ],
        default_layout="sky15",
    )
    assert [t["id"] for t in converted["tracks"]] == ["left", "right"]

    profile = PlaybackProfile(
        speed_percent=100,
        hold_min_ms=150,
        same_key_min_gap_ms=110,
        tap_press_ms=14,
        long_note_release_early_ms=80,
    )
    close_same_key_project = normalize_project(
        {
            "songId": "merge",
            "title": "Merge",
            "playbackProfile": profile.to_dict(),
            "tracks": [
                {
                    "id": "merge_track",
                    "events": [
                        {"timeMs": 0, "durationMs": 100, "keys": ["y"]},
                        {"timeMs": 50, "durationMs": 200, "keys": ["y"]},
                        {"timeMs": 500, "durationMs": 100, "keys": ["u"]},
                    ],
                }
            ],
        }
    )
    merged_actions = build_actions(close_same_key_project["tracks"], close_same_key_project["playbackProfile"])
    assert merged_actions[:2] == [
        PlaybackAction(0, "y", True),
        PlaybackAction(170, "y", False),
    ], merged_actions
    assert PlaybackAction(500, "u", True) in merged_actions
    assert PlaybackAction(514, "u", False) in merged_actions
    sliced_actions = slice_actions_from_position(merged_actions, 100)
    assert sliced_actions[0] == PlaybackAction(0, "y", True), sliced_actions
    assert PlaybackAction(70, "y", False) in sliced_actions, sliced_actions

    project = normalize_project(
        {
            "songId": "verify",
            "title": "Verify",
            "playbackProfile": profile.to_dict(),
            "tracks": [track_a, track_b],
        }
    )
    actions = build_actions(project["tracks"], project["playbackProfile"])
    assert actions, "expected playback actions"
    engine = PlaybackEngine(DryRunBackend(echo=False), time_scale=0.0)
    progress_samples = []
    engine.play(actions, start_monotonic_ms=0, on_progress=lambda p, d: progress_samples.append((p, d)))
    assert progress_samples[-1][0] == progress_samples[-1][1]
    seek_backend = DryRunBackend(echo=False)
    seek_engine = PlaybackEngine(seek_backend, time_scale=0.0)
    seek_engine.play(
        sliced_actions,
        start_monotonic_ms=0,
        position_offset_ms=100,
        total_duration_ms=actions[-1].time_ms if actions else 0,
    )
    assert seek_backend.actions[0] == ("down", "y")
    print("VERIFY_OK")
    print(f"tracks={len(project['tracks'])} actions={len(actions)}")


if __name__ == "__main__":
    main()
