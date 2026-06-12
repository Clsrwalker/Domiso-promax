#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pathlib

import numpy as np
from scipy.io import wavfile
import torch

from demucs.apply import BagOfModels, apply_model
from demucs.audio import AudioFile
from demucs.htdemucs import HTDemucs
from demucs.pretrained import get_model


def load_track(track: pathlib.Path, audio_channels: int, samplerate: int) -> torch.Tensor:
    try:
        return AudioFile(track).read(streams=0, samplerate=samplerate, channels=audio_channels)
    except FileNotFoundError as exc:
        raise RuntimeError("ffmpeg is required to read the input audio") from exc
    except Exception as exc:  # pragma: no cover - runtime codec edge cases
        raise RuntimeError(f"failed to read audio: {track}") from exc


def prevent_clip(wav: torch.Tensor, mode: str) -> torch.Tensor:
    if mode == "none":
        return wav
    if mode == "rescale":
        peak = max(float(wav.abs().max()), 1.0)
        return wav / (1.01 * peak)
    if mode == "clamp":
        return wav.clamp(-0.99, 0.99)
    raise ValueError(f"invalid clip mode: {mode}")


def save_wav_pcm16(path: pathlib.Path, wav: torch.Tensor, samplerate: int, clip_mode: str) -> None:
    wav = prevent_clip(wav, clip_mode)
    pcm = wav.detach().cpu().numpy().T
    pcm = np.clip(pcm, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(path, samplerate, pcm)


def run(
    input_audio: pathlib.Path,
    out_dir: pathlib.Path,
    model_name: str,
    device: str,
    shifts: int,
    jobs: int,
    overlap: float,
    clip_mode: str,
    cache_dir: pathlib.Path,
) -> pathlib.Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["TORCH_HOME"] = str(cache_dir)
    os.environ["XDG_CACHE_HOME"] = str(cache_dir)

    model = get_model(model_name)
    max_allowed_segment = float("inf")
    if isinstance(model, HTDemucs):
        max_allowed_segment = float(model.segment)
    elif isinstance(model, BagOfModels):
        max_allowed_segment = model.max_allowed_segment

    model.cpu()
    model.eval()

    wav = load_track(input_audio, model.audio_channels, model.samplerate)
    ref = wav.mean(0)
    wav = wav - ref.mean()
    wav = wav / ref.std()

    sources = apply_model(
        model,
        wav[None],
        device=device,
        shifts=shifts,
        split=True,
        overlap=overlap,
        progress=True,
        num_workers=jobs,
        segment=max_allowed_segment if max_allowed_segment != float("inf") else None,
    )[0]
    sources = sources * ref.std()
    sources = sources + ref.mean()

    stem_dir = out_dir / model_name / input_audio.stem
    stem_dir.mkdir(parents=True, exist_ok=True)
    for source, name in zip(sources, model.sources):
        save_wav_pcm16(stem_dir / f"{name}.wav", source, model.samplerate, clip_mode)
    return stem_dir


def main() -> None:
    ap = argparse.ArgumentParser(description="Separate audio with Demucs and save WAV stems without torchaudio.save.")
    ap.add_argument("input_audio")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--model", default="htdemucs_ft")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--shifts", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=0)
    ap.add_argument("--overlap", type=float, default=0.25)
    ap.add_argument("--clip-mode", choices=["rescale", "clamp", "none"], default="rescale")
    ap.add_argument("--cache-dir", required=True)
    args = ap.parse_args()

    stem_dir = run(
        pathlib.Path(args.input_audio).expanduser().resolve(),
        pathlib.Path(args.out_dir).expanduser().resolve(),
        args.model,
        args.device,
        args.shifts,
        args.jobs,
        args.overlap,
        args.clip_mode,
        pathlib.Path(args.cache_dir).expanduser().resolve(),
    )
    print(stem_dir)


if __name__ == "__main__":
    main()
