from __future__ import annotations

import argparse
import json
from pathlib import Path

from .domiso_sheet import read_sheet_file
from .midi_import import midi_to_project
from .project import load_project, project_from_domiso_tracks, save_project
from .playback import PlaybackProfile, build_actions


def command_from_domiso(args: argparse.Namespace) -> None:
    tracks = []
    for index, path_text in enumerate(args.inputs, start=1):
        path = Path(path_text)
        text, source = read_sheet_file(path, encoding=args.encoding)
        tracks.append(
            {
                "id": f"track_{index}",
                "name": path.stem,
                "layout": args.layout,
                "text": text,
                "fileName": path.name,
                "source": source,
            }
        )
    song_id = args.song_id or Path(args.output).stem
    playback_profile = PlaybackProfile(
        speed_percent=args.speed_percent,
        hold_min_ms=args.hold_min_ms,
        same_key_min_gap_ms=args.same_key_min_gap_ms,
        tap_press_ms=args.tap_press_ms,
        long_note_release_early_ms=args.release_early_ms,
    ).to_dict()
    project = project_from_domiso_tracks(
        song_id=song_id,
        title=args.title or song_id,
        tracks=tracks,
        default_layout=args.layout,
        pitch_naming=args.pitch_naming,
        playback_profile=playback_profile,
    )
    save_project(project, args.output)
    print(f"project={args.output}")
    print(f"tracks={len(project['tracks'])}")


def command_from_midi(args: argparse.Namespace) -> None:
    playback_profile = PlaybackProfile(
        speed_percent=args.speed_percent,
        hold_min_ms=args.hold_min_ms,
        same_key_min_gap_ms=args.same_key_min_gap_ms,
        tap_press_ms=args.tap_press_ms,
        long_note_release_early_ms=args.release_early_ms,
    ).to_dict()
    song_id = args.song_id or Path(args.output).stem
    project = midi_to_project(
        data=Path(args.input).read_bytes(),
        song_id=song_id,
        title=args.title or song_id,
        layout=args.layout,
        playback_profile=playback_profile,
    )
    save_project(project, args.output)
    print(f"project={args.output}")
    print(f"tracks={len(project['tracks'])}")


def command_inspect(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    profile = project.get("playbackProfile")
    tracks = project.get("tracks", [])
    print(f"songId={project.get('songId')}")
    print(f"title={project.get('title')}")
    print(f"playbackProfile={json.dumps(profile, ensure_ascii=False)}")
    print(f"tracks={len(tracks)}")
    for track in tracks:
        actions = build_actions([track], profile)
        print(
            f"- {track.get('id')}: {track.get('name')} "
            f"events={len(track.get('events', []))} actions={len(actions)} layout={track.get('layout')}"
        )
        stats = track.get("stats")
        if isinstance(stats, dict):
            print(
                "  stats "
                f"noteEvents={stats.get('noteEvents')} "
                f"keyEvents={stats.get('keyEvents')} "
                f"skipped={stats.get('skippedUnmappedNotes')} "
                f"durationMs={stats.get('durationMs')}"
            )


def command_print(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    print(json.dumps(project, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser(description="Create and inspect Domiso Orchestra project files.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_from = sub.add_parser("from-domiso", help="Create a multi-track project from one or more Domiso txt files.")
    p_from.add_argument("output")
    p_from.add_argument("inputs", nargs="+")
    p_from.add_argument("--song-id", default="")
    p_from.add_argument("--title", default="")
    p_from.add_argument("--layout", default="sky15", choices=["sky15", "domiso36"])
    p_from.add_argument("--pitch-naming", default="standard", choices=["standard", "domiso"])
    p_from.add_argument("--encoding", default="utf-8")
    p_from.add_argument("--speed-percent", type=float, default=95.0)
    p_from.add_argument("--hold-min-ms", type=int, default=150)
    p_from.add_argument("--same-key-min-gap-ms", type=int, default=110)
    p_from.add_argument("--tap-press-ms", type=int, default=14)
    p_from.add_argument("--release-early-ms", type=int, default=80)
    p_from.set_defaults(func=command_from_domiso)

    p_midi = sub.add_parser("from-midi", help="Create a multi-track project from a Standard MIDI file.")
    p_midi.add_argument("output")
    p_midi.add_argument("input")
    p_midi.add_argument("--song-id", default="")
    p_midi.add_argument("--title", default="")
    p_midi.add_argument("--layout", default="domiso36", choices=["sky15", "domiso36"])
    p_midi.add_argument("--speed-percent", type=float, default=95.0)
    p_midi.add_argument("--hold-min-ms", type=int, default=150)
    p_midi.add_argument("--same-key-min-gap-ms", type=int, default=110)
    p_midi.add_argument("--tap-press-ms", type=int, default=14)
    p_midi.add_argument("--release-early-ms", type=int, default=80)
    p_midi.set_defaults(func=command_from_midi)

    p_inspect = sub.add_parser("inspect")
    p_inspect.add_argument("project")
    p_inspect.set_defaults(func=command_inspect)

    p_print = sub.add_parser("print")
    p_print.add_argument("project")
    p_print.set_defaults(func=command_print)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
