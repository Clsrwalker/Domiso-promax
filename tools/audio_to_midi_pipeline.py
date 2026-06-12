#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import mido


DEFAULT_BACKEND_PYTHON = pathlib.Path(r"D:\basic-pitch\basic-pitch\.venv\Scripts\python.exe")
DEFAULT_BASIC_PITCH_REPO = pathlib.Path(r"D:\basic-pitch\basic-pitch")
DEFAULT_OUT_DIR = pathlib.Path(r"D:\domiso\audio_pipeline")
DEFAULT_DEMUCS_CACHE_DIR = pathlib.Path(r"D:\domiso\third_party\demucs_cache\torch")


@dataclass(frozen=True)
class TranscribePreset:
    onset_threshold: float
    frame_threshold: float
    minimum_note_length_ms: float
    infer_onsets: bool
    melodia_trick: bool
    minimum_frequency: Optional[float] = None
    maximum_frequency: Optional[float] = None


PRESETS: Dict[str, TranscribePreset] = {
    "neuralnote_compat": TranscribePreset(0.50, 0.30, 127.7, True, True, None, None),
    "vocals_lead": TranscribePreset(0.54, 0.34, 140.0, True, True, 110.0, 1400.0),
    "other_clean": TranscribePreset(0.64, 0.40, 220.0, False, False, 65.0, 1800.0),
    "other_loose": TranscribePreset(0.58, 0.36, 180.0, False, False, 55.0, 2200.0),
    "full_mix_soft": TranscribePreset(0.68, 0.42, 240.0, False, False, 80.0, 1600.0),
}


def run_cmd(
    cmd: List[str],
    cwd: Optional[pathlib.Path] = None,
    env: Optional[dict] = None,
    stream: bool = False,
) -> str:
    if stream:
        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd) if cwd else None,
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
            raise RuntimeError(f"command interrupted and child process tree was terminated\nCMD: {' '.join(cmd)}") from exc
        if returncode != 0:
            raise RuntimeError(f"command failed with exit code {returncode}\nCMD: {' '.join(cmd)}")
        return ""

    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    if proc.returncode != 0:
        msg = proc.stderr.strip() or proc.stdout.strip() or "command failed"
        raise RuntimeError(f"{msg}\nCMD: {' '.join(cmd)}")
    return proc.stdout.strip()


def resolve_backend_python(path: Optional[str]) -> pathlib.Path:
    exe = pathlib.Path(path).expanduser().resolve() if path else DEFAULT_BACKEND_PYTHON
    if not exe.exists():
        raise FileNotFoundError(f"backend python not found: {exe}")
    return exe


def resolve_basic_pitch_repo(path: Optional[str]) -> pathlib.Path:
    repo = pathlib.Path(path).expanduser().resolve() if path else DEFAULT_BASIC_PITCH_REPO
    if not repo.exists():
        raise FileNotFoundError(f"basic-pitch repo not found: {repo}")
    return repo


def song_base_name(audio_path: pathlib.Path) -> str:
    return audio_path.stem


def ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg not found in PATH")


def separate_with_demucs(
    backend_python: pathlib.Path,
    helper_script: pathlib.Path,
    input_audio: pathlib.Path,
    out_dir: pathlib.Path,
    model: str,
    device: str,
    shifts: int,
    jobs: int,
    cache_dir: pathlib.Path,
) -> pathlib.Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(backend_python),
        str(helper_script),
        str(input_audio),
        "--out-dir",
        str(out_dir),
        "--model",
        model,
        "--device",
        device,
        "--shifts",
        str(shifts),
        "--jobs",
        str(jobs),
        "--cache-dir",
        str(cache_dir),
    ]
    run_cmd(cmd, stream=True)
    return out_dir / model / input_audio.stem


def transcribe_audio(
    backend_python: pathlib.Path,
    helper_script: pathlib.Path,
    basic_pitch_repo: pathlib.Path,
    audio_path: pathlib.Path,
    output_midi: pathlib.Path,
    preset: TranscribePreset,
    midi_tempo: float,
) -> str:
    cmd = [
        str(backend_python),
        str(helper_script),
        str(audio_path),
        str(output_midi),
        "--basic-pitch-repo",
        str(basic_pitch_repo),
        "--onset-threshold",
        str(preset.onset_threshold),
        "--frame-threshold",
        str(preset.frame_threshold),
        "--minimum-note-length",
        str(preset.minimum_note_length_ms),
        "--infer-onsets",
        "true" if preset.infer_onsets else "false",
        "--melodia-trick",
        "true" if preset.melodia_trick else "false",
        "--midi-tempo",
        str(midi_tempo),
    ]
    if preset.minimum_frequency is not None:
        cmd += ["--minimum-frequency", str(preset.minimum_frequency)]
    if preset.maximum_frequency is not None:
        cmd += ["--maximum-frequency", str(preset.maximum_frequency)]
    return run_cmd(cmd, stream=True)


def list_existing_stems(stem_dir: pathlib.Path) -> Dict[str, pathlib.Path]:
    out: Dict[str, pathlib.Path] = {}
    for stem in ("vocals", "other", "bass", "drums", "no_vocals", "piano", "guitar"):
        for ext in (".wav", ".mp3", ".flac"):
            candidate = stem_dir / f"{stem}{ext}"
            if candidate.exists():
                out[stem] = candidate
                break
    return out


def merge_midis(midi_paths: Iterable[pathlib.Path], out_path: pathlib.Path) -> None:
    midi_paths = list(midi_paths)
    if not midi_paths:
        raise RuntimeError("no midi files to merge")

    first = mido.MidiFile(str(midi_paths[0]))
    merged = mido.MidiFile(ticks_per_beat=first.ticks_per_beat)

    meta_added = False
    for path in midi_paths:
        mid = mido.MidiFile(str(path))
        for idx, track in enumerate(mid.tracks):
            msgs = list(track)
            if not meta_added:
                meta = mido.MidiTrack()
                for msg in msgs:
                    if msg.is_meta and msg.type in {"set_tempo", "time_signature", "key_signature", "track_name"}:
                        meta.append(msg.copy())
                if not meta:
                    meta.append(mido.MetaMessage("track_name", name="meta", time=0))
                merged.tracks.append(meta)
                meta_added = True
            if idx == 0:
                note_track = mido.MidiTrack()
                note_track.append(mido.MetaMessage("track_name", name=path.stem, time=0))
                appended = False
                for msg in msgs:
                    if msg.is_meta:
                        continue
                    note_track.append(msg.copy())
                    appended = True
                if appended:
                    merged.tracks.append(note_track)
            else:
                merged.tracks.append(mido.MidiTrack(msg.copy() for msg in msgs))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.save(str(out_path))


def write_report(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_report(path: pathlib.Path) -> Optional[dict]:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def preset_summary(preset: TranscribePreset) -> dict:
    return {
        "onset_threshold": preset.onset_threshold,
        "frame_threshold": preset.frame_threshold,
        "minimum_note_length_ms": preset.minimum_note_length_ms,
        "infer_onsets": preset.infer_onsets,
        "melodia_trick": preset.melodia_trick,
        "minimum_frequency": preset.minimum_frequency,
        "maximum_frequency": preset.maximum_frequency,
    }


def print_status(report: Optional[dict], report_path: pathlib.Path) -> None:
    if not report:
        print(f"report_missing={report_path}")
        return
    print(f"report={report_path}")
    print(f"status={report.get('status', 'unknown')}")
    print(f"song_dir={report.get('song_dir', '')}")
    stages = report.get("stages", {})
    print(f"stage_separation={stages.get('separation', 'unknown')}")
    for stem_name, stem_status in stages.get("transcriptions", {}).items():
        print(f"stage_transcribe_{stem_name}={stem_status}")
    print(f"stage_merge={stages.get('merge', 'unknown')}")
    for target, target_status in stages.get("domiso", {}).items():
        print(f"stage_domiso_{target}={target_status}")


def ensure_stage_inputs(stage_name: str, inputs: Dict[str, pathlib.Path], required: List[str]) -> None:
    missing = [name for name in required if name not in inputs or not inputs[name].exists()]
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"{stage_name} missing required inputs: {joined}")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Automatic pop-song pipeline: Demucs separation -> stem MIDI transcription -> optional merged MIDI / DoMiSo."
    )
    ap.add_argument("input_audio")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    ap.add_argument("--backend-python", default=None, help="Python executable with demucs + onnxruntime installed.")
    ap.add_argument("--basic-pitch-repo", default=None)
    ap.add_argument("--demucs-cache-dir", default=str(DEFAULT_DEMUCS_CACHE_DIR))
    ap.add_argument("--demucs-model", default="htdemucs_ft")
    ap.add_argument("--demucs-device", default="cpu")
    ap.add_argument("--demucs-shifts", type=int, default=1)
    ap.add_argument("--demucs-jobs", type=int, default=0)
    ap.add_argument("--skip-separation", action="store_true")
    ap.add_argument("--transcribe-stems", nargs="*", default=["vocals", "other"])
    ap.add_argument("--vocals-preset", choices=sorted(PRESETS), default="vocals_lead")
    ap.add_argument("--other-preset", choices=sorted(PRESETS), default="other_clean")
    ap.add_argument("--default-preset", choices=sorted(PRESETS), default="neuralnote_compat")
    ap.add_argument("--midi-tempo", type=float, default=120.0)
    ap.add_argument("--merge-midi", action="store_true", default=True)
    ap.add_argument("--no-merge-midi", action="store_false", dest="merge_midi")
    ap.add_argument("--run-domiso-on", nargs="*", default=[], help="midi targets to run domiso_generate_all on: vocals other merged")
    ap.add_argument("--resume", action="store_true", default=True, help="Reuse finished stems/MIDI files when they already exist.")
    ap.add_argument("--no-resume", action="store_false", dest="resume")
    ap.add_argument("--status-only", action="store_true", help="Print the current pipeline report and exit.")
    ap.add_argument(
        "--stage",
        choices=["all", "separate", "transcribe", "merge", "domiso"],
        default="all",
        help="Run only one pipeline stage, or all stages.",
    )
    args = ap.parse_args()

    ensure_ffmpeg()

    input_audio = pathlib.Path(args.input_audio).expanduser().resolve()
    if not input_audio.exists():
        raise FileNotFoundError(f"input audio not found: {input_audio}")

    backend_python = resolve_backend_python(args.backend_python)
    basic_pitch_repo = resolve_basic_pitch_repo(args.basic_pitch_repo)
    helper_script = pathlib.Path(__file__).with_name("audio_transcribe_basic_pitch.py")
    demucs_helper = pathlib.Path(__file__).with_name("audio_separate_demucs.py")
    domiso_generate = pathlib.Path(__file__).with_name("domiso_generate_all.py")

    song_dir = pathlib.Path(args.out_dir).expanduser().resolve() / song_base_name(input_audio)
    stems_root = song_dir / "stems"
    midi_root = song_dir / "mid"
    demucs_cache_dir = pathlib.Path(args.demucs_cache_dir).expanduser().resolve()
    report_path = song_dir / "pipeline_report.json"
    song_dir.mkdir(parents=True, exist_ok=True)
    expected_stem_dir = stems_root / args.demucs_model / input_audio.stem
    if args.status_only:
        print_status(read_report(report_path), report_path)
        return

    report = {
        "status": "running",
        "input_audio": str(input_audio),
        "song_dir": str(song_dir),
        "backend_python": str(backend_python),
        "basic_pitch_repo": str(basic_pitch_repo),
        "demucs_model": args.demucs_model,
        "demucs_device": args.demucs_device,
        "demucs_cache_dir": str(demucs_cache_dir),
        "stages": {
            "separation": "pending",
            "transcriptions": {},
            "merge": "pending" if args.merge_midi else "disabled",
            "domiso": {},
        },
    }
    write_report(report_path, report)

    stems: Dict[str, pathlib.Path] = {}
    if args.stage not in {"all", "separate"} and expected_stem_dir.exists():
        stems = list_existing_stems(expected_stem_dir)
        if stems:
            stem_dir = expected_stem_dir
            report["stem_dir"] = str(stem_dir)
            report["stages"]["separation"] = "existing"
        else:
            stem_dir = expected_stem_dir
    if args.stage in {"all", "separate"} and args.skip_separation:
        stem_dir = expected_stem_dir
        report["stages"]["separation"] = "skipped"
    elif args.stage in {"all", "separate"} and args.resume and list_existing_stems(expected_stem_dir):
        print(f"[1/4] Reusing existing stems: {expected_stem_dir}")
        stem_dir = expected_stem_dir
        report["stages"]["separation"] = "reused"
    elif args.stage in {"all", "separate"}:
        print(f"[1/4] Separating with Demucs: {input_audio.name}")
        stem_dir = separate_with_demucs(
            backend_python,
            demucs_helper,
            input_audio,
            stems_root,
            args.demucs_model,
            args.demucs_device,
            args.demucs_shifts,
            args.demucs_jobs,
            demucs_cache_dir,
        )
        report["stages"]["separation"] = "done"
    if args.stage in {"all", "separate"}:
        report["stem_dir"] = str(stem_dir)
        write_report(report_path, report)
        stems = list_existing_stems(stem_dir)
        if not stems:
            report["status"] = "failed"
            report["error"] = f"no stems found in {stem_dir}"
            write_report(report_path, report)
            raise RuntimeError(f"no stems found in {stem_dir}")
        if args.stage == "separate":
            report["status"] = "done"
            report["stems_found"] = {k: str(v) for k, v in stems.items()}
            write_report(report_path, report)
            print(f"song_dir={song_dir}")
            print(f"stem_dir={stem_dir}")
            print(f"report={report_path}")
            return

    generated_midis: Dict[str, pathlib.Path] = {}
    transcribe_logs: Dict[str, dict] = {}
    transcribe_total = len(args.transcribe_stems)
    if args.stage in {"all", "transcribe"}:
        if not stems:
            stems = list_existing_stems(expected_stem_dir)
        if not stems:
            report["status"] = "failed"
            report["error"] = f"transcribe requires stems in {expected_stem_dir}"
            write_report(report_path, report)
            raise RuntimeError(f"transcribe requires stems in {expected_stem_dir}")
        for index, stem_name in enumerate(args.transcribe_stems, start=1):
            audio_path = stems.get(stem_name)
            if not audio_path:
                continue
            if stem_name == "vocals":
                preset = PRESETS[args.vocals_preset]
            elif stem_name == "other":
                preset = PRESETS[args.other_preset]
            else:
                preset = PRESETS[args.default_preset]
            out_midi = midi_root / f"{input_audio.stem}_{stem_name}.mid"
            transcribe_logs[stem_name] = {
                "audio": str(audio_path),
                "output_midi": str(out_midi),
                "preset": preset_summary(preset),
            }
            if args.resume and out_midi.exists():
                print(f"[2/4] Reusing MIDI {index}/{transcribe_total}: {out_midi.name}")
                report["stages"]["transcriptions"][stem_name] = "reused"
            else:
                print(f"[2/4] Transcribing stem {index}/{transcribe_total}: {stem_name} -> {out_midi.name}")
                transcribe_audio(
                    backend_python,
                    helper_script,
                    basic_pitch_repo,
                    audio_path,
                    out_midi,
                    preset,
                    args.midi_tempo,
                )
                report["stages"]["transcriptions"][stem_name] = "done"
            generated_midis[stem_name] = out_midi
            write_report(report_path, report)
        if args.stage == "transcribe":
            report["status"] = "done"
            report["generated_midis"] = {k: str(v) for k, v in generated_midis.items()}
            report["transcribe_logs"] = transcribe_logs
            write_report(report_path, report)
            print(f"song_dir={song_dir}")
            for name, midi_path in generated_midis.items():
                print(f"midi_{name}={midi_path}")
            print(f"report={report_path}")
            return
    else:
        for stem_name in args.transcribe_stems:
            out_midi = midi_root / f"{input_audio.stem}_{stem_name}.mid"
            if out_midi.exists():
                generated_midis[stem_name] = out_midi

    merged_midi = None
    if args.stage in {"all", "merge"} and args.merge_midi and generated_midis:
        merge_order = [name for name in ("vocals", "other", "bass") if name in generated_midis]
        merge_order += [name for name in generated_midis if name not in merge_order]
        merged_midi = midi_root / f"{input_audio.stem}_merged.mid"
        if args.resume and merged_midi.exists():
            print(f"[3/4] Reusing merged MIDI: {merged_midi.name}")
            report["stages"]["merge"] = "reused"
        else:
            print(f"[3/4] Merging MIDI tracks -> {merged_midi.name}")
            merge_midis([generated_midis[name] for name in merge_order], merged_midi)
            report["stages"]["merge"] = "done"
        generated_midis["merged"] = merged_midi
        write_report(report_path, report)
        if args.stage == "merge":
            report["status"] = "done"
            report["generated_midis"] = {k: str(v) for k, v in generated_midis.items()}
            write_report(report_path, report)
            print(f"song_dir={song_dir}")
            print(f"midi_merged={merged_midi}")
            print(f"report={report_path}")
            return
    elif args.stage == "merge":
        report["status"] = "failed"
        report["error"] = "merge stage requires existing stem MIDI files"
        write_report(report_path, report)
        raise RuntimeError("merge stage requires existing stem MIDI files")
    elif args.merge_midi:
        merged_candidate = midi_root / f"{input_audio.stem}_merged.mid"
        if merged_candidate.exists():
            generated_midis["merged"] = merged_candidate

    domiso_outputs = {}
    domiso_total = len(args.run_domiso_on)
    if args.stage in {"all", "domiso"}:
        if args.stage == "domiso":
            for target in args.run_domiso_on:
                midi_path = midi_root / f"{input_audio.stem}_{target}.mid"
                if target == "merged":
                    midi_path = midi_root / f"{input_audio.stem}_merged.mid"
                if midi_path.exists():
                    generated_midis[target] = midi_path
        for index, target in enumerate(args.run_domiso_on, start=1):
            midi_path = generated_midis.get(target)
            if not midi_path:
                continue
            print(f"[4/4] Running DoMiSo generation {index}/{domiso_total}: {target} -> {midi_path.name}")
            run_cmd(
                [
                    sys.executable,
                    str(domiso_generate),
                    str(midi_path),
                    "--out-dir",
                    str(pathlib.Path(r"D:\domiso\txt")),
                    "--report-dir",
                    str(pathlib.Path(r"D:\domiso\txt")),
                ]
                ,
                stream=True,
            )
            domiso_outputs[target] = {
                "input_midi": str(midi_path),
                "out_dir": str(pathlib.Path(r"D:\domiso\txt")),
            }
            report["stages"]["domiso"][target] = "done"
            write_report(report_path, report)
        if args.stage == "domiso":
            report["status"] = "done"
            report["domiso_outputs"] = domiso_outputs
            write_report(report_path, report)
            print(f"song_dir={song_dir}")
            print(f"report={report_path}")
            return

    report["status"] = "done"
    report["stems_found"] = {k: str(v) for k, v in stems.items()}
    report["generated_midis"] = {k: str(v) for k, v in generated_midis.items()}
    report["transcribe_logs"] = transcribe_logs
    report["domiso_outputs"] = domiso_outputs
    write_report(report_path, report)

    print(f"song_dir={song_dir}")
    print(f"stem_dir={stem_dir}")
    for name, midi_path in generated_midis.items():
        print(f"midi_{name}={midi_path}")
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
