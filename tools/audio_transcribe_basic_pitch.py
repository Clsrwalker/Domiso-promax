#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess
import sys
from typing import Optional


def _resolve_repo(repo: Optional[str]) -> pathlib.Path:
    if repo:
        path = pathlib.Path(repo).expanduser().resolve()
    else:
        path = pathlib.Path(r"D:\basic-pitch\basic-pitch")
    if not path.exists():
        raise FileNotFoundError(f"basic-pitch repo not found: {path}")
    return path


def _bool_flag(value: str) -> bool:
    v = value.strip().lower()
    if v in {"1", "true", "yes", "on"}:
        return True
    if v in {"0", "false", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid boolean: {value}")


def _run(cmd: list[str], env: dict) -> None:
    proc = subprocess.Popen(
        cmd,
        env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
    )
    try:
        returncode = proc.wait()
    except KeyboardInterrupt as exc:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                capture_output=True,
                text=True,
            )
        else:
            proc.kill()
        raise RuntimeError("basic_pitch.predict interrupted and child process tree was terminated") from exc
    if returncode != 0:
        raise RuntimeError(f"basic_pitch.predict failed with exit code {returncode}")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Transcribe one audio file to MIDI by delegating to the official basic_pitch.predict CLI."
    )
    ap.add_argument("input_audio")
    ap.add_argument("output_midi")
    ap.add_argument("--basic-pitch-repo", default=None)
    ap.add_argument("--model-path", default=None)
    ap.add_argument("--onset-threshold", type=float, default=0.5)
    ap.add_argument("--frame-threshold", type=float, default=0.3)
    ap.add_argument("--minimum-note-length", type=float, default=127.7, help="milliseconds")
    ap.add_argument("--minimum-frequency", type=float, default=None)
    ap.add_argument("--maximum-frequency", type=float, default=None)
    ap.add_argument("--infer-onsets", type=_bool_flag, default=True)
    ap.add_argument("--melodia-trick", type=_bool_flag, default=True)
    ap.add_argument("--multiple-pitch-bends", type=_bool_flag, default=False)
    ap.add_argument("--midi-tempo", type=float, default=120.0)
    args = ap.parse_args()

    repo = _resolve_repo(args.basic_pitch_repo)
    input_audio = pathlib.Path(args.input_audio).expanduser().resolve()
    output_midi = pathlib.Path(args.output_midi).expanduser().resolve()
    if not input_audio.exists():
        raise FileNotFoundError(f"input audio not found: {input_audio}")
    output_midi.parent.mkdir(parents=True, exist_ok=True)

    generated_midi = output_midi.parent / f"{input_audio.stem}_basic_pitch.mid"
    if generated_midi.exists():
        generated_midi.unlink()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env["PYTHONIOENCODING"] = "utf-8"

    cmd = [
        sys.executable,
        "-m",
        "basic_pitch.predict",
        "--model-serialization",
        "onnx",
        "--save-midi",
        "--onset-threshold",
        str(args.onset_threshold),
        "--frame-threshold",
        str(args.frame_threshold),
        "--minimum-note-length",
        str(args.minimum_note_length),
        "--midi-tempo",
        str(args.midi_tempo),
    ]
    if args.minimum_frequency is not None:
        cmd += ["--minimum-frequency", str(args.minimum_frequency)]
    if args.maximum_frequency is not None:
        cmd += ["--maximum-frequency", str(args.maximum_frequency)]
    if args.multiple_pitch_bends:
        cmd += ["--multiple-pitch-bends"]
    if not args.melodia_trick:
        cmd += ["--no-melodia"]
    if args.model_path:
        cmd += ["--model-path", str(pathlib.Path(args.model_path).expanduser().resolve())]
    cmd += [str(output_midi.parent), str(input_audio)]

    print(f"[basic-pitch-cli] input={input_audio.name}")
    print(f"[basic-pitch-cli] output_dir={output_midi.parent}")
    if not args.infer_onsets:
        print("[basic-pitch-cli] note: infer_onsets is not exposed by official CLI and is ignored in this backend.")

    _run(cmd, env)

    if not generated_midi.exists():
        raise FileNotFoundError(f"expected basic_pitch output not found: {generated_midi}")

    if output_midi.exists():
        output_midi.unlink()
    shutil.move(str(generated_midi), str(output_midi))

    print(f"output={output_midi}")
    print(
        "settings="
        f"onset:{args.onset_threshold},frame:{args.frame_threshold},"
        f"min_ms:{args.minimum_note_length},infer_onsets:{args.infer_onsets},"
        f"melodia:{args.melodia_trick},tempo:{args.midi_tempo}"
    )


if __name__ == "__main__":
    main()
