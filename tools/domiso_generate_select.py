#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import locale
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class ScriptSpec:
    name: str
    target: str
    args: Sequence[str]


def _decode_output(buf: bytes) -> str:
    if not buf:
        return ""
    for enc in ("utf-8", locale.getpreferredencoding(False), "gbk", "mbcs"):
        try:
            return buf.decode(enc)
        except Exception:
            continue
    return buf.decode("utf-8", errors="replace")


def _safe_stem(path: str) -> str:
    stem = Path(path).stem
    for ch in '<>:"/\\|?*':
        stem = stem.replace(ch, "_")
    return stem.strip(" .") or "midi"


def _write_json(path: str | None, data: dict) -> None:
    if not path:
        return
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(target)


def _run_cmd(cmd: List[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=False)
    return p.returncode, _decode_output(p.stdout), _decode_output(p.stderr)


def _registry(tool_dir: str, input_midi: str, out_dir: str, report_dir: str) -> list[ScriptSpec]:
    def pipeline(script: str, name: str, target: str) -> ScriptSpec:
        return ScriptSpec(
            name=name,
            target=target,
            args=[
                os.path.join(tool_dir, script),
                "pipeline",
                input_midi,
                "--profile",
                "auto",
                "--out-dir",
                out_dir,
                "--report-dir",
                report_dir,
            ],
        )

    def direct(script: str, name: str, target: str) -> ScriptSpec:
        return ScriptSpec(
            name=name,
            target=target,
            args=[
                os.path.join(tool_dir, script),
                input_midi,
                "--profile",
                "auto",
                "--out-dir",
                out_dir,
            ],
        )

    def direct_sky(script: str, name: str) -> ScriptSpec:
        return direct(script, name, "sky")

    return [
        ScriptSpec(
            "dense3layer",
            "genshin",
            [os.path.join(tool_dir, "midi_to_domiso_dense3layer.py"), input_midi, "--out-dir", out_dir],
        ),
        pipeline("domiso_pipeline.py", "basic", "genshin"),
        pipeline("domiso_pipeline_longnote.py", "longnote", "genshin"),
        pipeline("domiso_pipeline_longnote_human.py", "longnote_human", "genshin"),
        pipeline("domiso_pipeline_longnote_human_v2.py", "longnote_human_v2", "genshin"),
        pipeline("domiso_pipeline_restore.py", "restore", "genshin"),
        pipeline("domiso_pipeline_literal.py", "literal", "genshin"),
        pipeline("domiso_pipeline_literal_melodylock.py", "literal_melodylock", "genshin"),
        direct(
            "domiso_pipeline_literal_melodylock_ensemble.py",
            "literal_melodylock_ensemble",
            "genshin",
        ),
        pipeline("domiso_pipeline_literal_transcription.py", "literal_transcription", "genshin"),
        pipeline("domiso_pipeline_literal_human.py", "literal_human", "genshin"),
        pipeline("domiso_pipeline_highlight.py", "highlight", "genshin"),
        pipeline("domiso_pipeline_sky_melodylock.py", "sky_melodylock", "sky"),
        pipeline("domiso_pipeline_sky_duet.py", "sky_duet", "sky"),
        pipeline("domiso_pipeline_sky_melodylock_human.py", "sky_melodylock_human", "sky"),
        pipeline("domiso_pipeline_sky_literal.py", "sky_literal", "sky"),
        pipeline("domiso_pipeline_sky_handpan_melodylock.py", "sky_handpan_melodylock", "sky"),
        direct_sky("domiso_pipeline_sky_violin_piano.py", "sky_violin_piano"),
        direct_sky("domiso_pipeline_sky_violin_piano_smooth.py", "sky_violin_piano_smooth"),
        direct_sky("domiso_pipeline_sky_violin_piano_interpreted.py", "sky_violin_piano_interpreted"),
        pipeline("domiso_pipeline_yihuan_melodylock.py", "yihuan_melodylock", "yihuan"),
        pipeline("domiso_pipeline_yihuan_restore36.py", "yihuan_restore36", "yihuan"),
        pipeline("domiso_pipeline_yihuan_noki_like.py", "yihuan_noki_like", "yihuan"),
        pipeline("domiso_pipeline_yihuan_midlead36.py", "yihuan_midlead36", "yihuan"),
        pipeline("domiso_pipeline_yihuan_ballad36.py", "yihuan_ballad36", "yihuan"),
        pipeline("domiso_pipeline_yihuan_lowlead36.py", "yihuan_lowlead36", "yihuan"),
        pipeline("domiso_pipeline_horn_literal.py", "horn_literal", "other"),
        pipeline("domiso_pipeline_guitar_literal.py", "guitar_literal", "other"),
        pipeline("domiso_pipeline_literal_arranged.py", "literal_arranged", "other"),
        pipeline("domiso_pipeline_guitar.py", "guitar", "other"),
        pipeline("domiso_pipeline_horn.py", "horn", "other"),
    ]


def _select_specs(specs: Iterable[ScriptSpec], target: str, scripts: str) -> list[ScriptSpec]:
    specs = list(specs)
    if target != "all":
        specs = [s for s in specs if s.target == target]
    if scripts:
        wanted = {x.strip().lower() for x in scripts.split(",") if x.strip()}
        specs = [s for s in specs if s.name.lower() in wanted]
    return specs


def _collect_outputs(out_dir: str, input_midi: str, since: float) -> list[str]:
    root = Path(out_dir)
    if not root.exists():
        return []
    safe = _safe_stem(input_midi).lower()
    candidates: list[Path] = []
    song_dir = root / _safe_stem(input_midi)
    search_roots = [song_dir] if song_dir.exists() else []
    search_roots.append(root)
    seen: set[Path] = set()
    for base in search_roots:
        try:
            iterator = base.rglob("*") if base == song_dir else base.glob(f"{safe}*")
            for p in iterator:
                if p in seen or not p.is_file():
                    continue
                seen.add(p)
                if p.suffix.lower() not in {".txt", ".md"}:
                    continue
                try:
                    mtime = p.stat().st_mtime
                except OSError:
                    continue
                if mtime >= since - 2:
                    candidates.append(p)
        except OSError:
            continue
    candidates.sort(key=lambda p: (p.suffix.lower() != ".txt", p.name.lower()))
    return [str(p) for p in candidates]


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate selected DoMiSo outputs for one MIDI.")
    ap.add_argument("input_midi", nargs="?", help="Input MIDI file")
    ap.add_argument("--target", choices=["all", "genshin", "sky", "yihuan", "other"], default="yihuan")
    ap.add_argument("--scripts", default="", help="Comma separated script names, optional")
    ap.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap.add_argument("--report-dir", default=r"d:\domiso\txt")
    ap.add_argument("--progress-file", default="")
    ap.add_argument("--manifest-file", default="")
    ap.add_argument("--stop-on-error", action="store_true")
    ap.add_argument("--list-scripts", action="store_true")
    args = ap.parse_args()

    tool_dir = os.path.dirname(os.path.abspath(__file__))
    if args.list_scripts:
        specs = _select_specs(
            _registry(tool_dir, args.input_midi or "input.mid", args.out_dir, args.report_dir),
            args.target,
            args.scripts,
        )
        for spec in specs:
            print(f"{spec.target}\t{spec.name}")
        return

    if not args.input_midi:
        raise SystemExit("input_midi is required")
    if not os.path.isfile(args.input_midi):
        raise FileNotFoundError(f"Input MIDI not found: {args.input_midi}")

    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    Path(args.report_dir).mkdir(parents=True, exist_ok=True)
    if not args.manifest_file:
        manifest_dir = Path(args.report_dir) / _safe_stem(args.input_midi)
        manifest_dir.mkdir(parents=True, exist_ok=True)
        args.manifest_file = str(manifest_dir / f"{_safe_stem(args.input_midi)}_generate_{args.target}_manifest.json")

    specs = _select_specs(_registry(tool_dir, args.input_midi, args.out_dir, args.report_dir), args.target, args.scripts)
    if not specs:
        raise SystemExit(f"No scripts selected for target={args.target!r} scripts={args.scripts!r}")

    state = {
        "input_midi": os.path.abspath(args.input_midi),
        "target": args.target,
        "out_dir": os.path.abspath(args.out_dir),
        "report_dir": os.path.abspath(args.report_dir),
        "status": "running",
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(specs),
        "current": 0,
        "entries": [],
        "outputs": [],
    }
    _write_json(args.progress_file, state)
    start_time = time.time()
    py = sys.executable
    any_error = False

    for i, spec in enumerate(specs, start=1):
        cmd = [py, *spec.args]
        state["current"] = i
        state["current_name"] = spec.name
        state["status"] = "running"
        _write_json(args.progress_file, state)
        print(f"[{i}/{len(specs)}] {spec.target}:{spec.name}")
        print(" ".join(cmd))
        before = time.time()
        code, stdout, stderr = _run_cmd(cmd)
        entry = {
            "index": i,
            "name": spec.name,
            "target": spec.target,
            "returncode": code,
            "ok": code == 0,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
            "outputs": _collect_outputs(args.out_dir, args.input_midi, before),
        }
        state["entries"].append(entry)
        if code != 0:
            any_error = True
            print(stderr.strip() or stdout.strip() or f"{spec.name} failed")
            if args.stop_on_error:
                break
        else:
            if stdout.strip():
                print(stdout.strip())
        state["outputs"] = _collect_outputs(args.out_dir, args.input_midi, start_time)
        _write_json(args.progress_file, state)

    state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    state["status"] = "failed" if any_error else "done"
    state["outputs"] = _collect_outputs(args.out_dir, args.input_midi, start_time)
    _write_json(args.progress_file, state)
    _write_json(args.manifest_file, state)
    print(f"MANIFEST={args.manifest_file}")
    print(f"STATUS={state['status']}")
    for p in state["outputs"]:
        print(f"OUTPUT={p}")
    if any_error:
        sys.exit(2)


if __name__ == "__main__":
    main()
