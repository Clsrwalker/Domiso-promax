#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import domiso_pipeline_sky_violin_piano as normal
import domiso_pipeline_sky_melodylock as sky


def run_pipeline(script_name: str, args: argparse.Namespace, extra: list[str]) -> None:
    cmd = [
        sys.executable,
        str(TOOLS_DIR / script_name),
    ]
    if args.midi:
        cmd.append(args.midi)
    cmd.extend(["--downloads", str(args.downloads)])
    cmd.extend(["--out-dir", str(args.out_dir)])
    cmd.extend(["--profile", args.profile])
    cmd.extend(["--violin-track", args.violin_track])
    cmd.extend(["--piano-tracks", args.piano_tracks])
    cmd.extend(["--piano-max-poly", str(args.piano_max_poly)])
    cmd.extend(extra)
    print("")
    print("RUN " + " ".join(f'"{part}"' if " " in part else part for part in cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate all Sky15 violin+piano versions for one MIDI: basic, smooth, interpreted."
    )
    parser.add_argument(
        "midi",
        nargs="?",
        help="Optional MIDI path or filename. If omitted, newest .mid/.midi in Downloads is used.",
    )
    parser.add_argument("--downloads", default=str(normal.default_downloads_dir()))
    parser.add_argument("--out-dir", default=str(ROOT_DIR / "txt"))
    parser.add_argument("--profile", default="auto", choices=["auto"] + sorted(sky.PROFILES))
    parser.add_argument("--violin-track", default="auto")
    parser.add_argument("--piano-tracks", default="auto")
    parser.add_argument("--piano-max-poly", default=4, type=int)
    parser.add_argument("--smooth-style", default="balanced", choices=["light", "balanced", "strong"])
    parser.add_argument("--interpreted-style", default="lyrical", choices=["faithful", "balanced", "lyrical"])
    args = parser.parse_args()

    resolved = normal.resolve_midi_path(args.midi, Path(args.downloads).expanduser())
    print(f"target_midi={resolved}")

    # Use the resolved full path for all three runs so every version targets the
    # same file even if Downloads changes while the pipelines are running.
    args.midi = str(resolved)

    run_pipeline("domiso_pipeline_sky_violin_piano.py", args, [])
    run_pipeline("domiso_pipeline_sky_violin_piano_smooth.py", args, ["--violin-style", args.smooth_style])
    run_pipeline(
        "domiso_pipeline_sky_violin_piano_interpreted.py",
        args,
        ["--violin-style", args.interpreted_style],
    )


if __name__ == "__main__":
    main()
