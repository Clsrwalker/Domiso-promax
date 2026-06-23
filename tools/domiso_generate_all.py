#!/usr/bin/env python3
from __future__ import annotations

import argparse
import locale
import os
import subprocess
import sys
from typing import List


def _decode_output(buf: bytes) -> str:
    if not buf:
        return ""
    for enc in ("utf-8", locale.getpreferredencoding(False), "gbk", "mbcs"):
        try:
            return buf.decode(enc)
        except Exception:
            continue
    return buf.decode("utf-8", errors="replace")


def run_cmd(cmd: List[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=False)
    out = _decode_output(p.stdout)
    err = _decode_output(p.stderr)
    if p.returncode != 0:
        msg = err.strip() or out.strip() or f"failed: {' '.join(cmd)}"
        raise RuntimeError(msg)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate all current DoMiSo script outputs for one MIDI."
    )
    ap.add_argument("input_midi")
    ap.add_argument("--out-dir", default=r"d:\domiso\txt")
    ap.add_argument("--report-dir", default=r"d:\domiso\txt")
    args = ap.parse_args()
    if not os.path.isfile(args.input_midi):
        raise FileNotFoundError(f"Input MIDI not found: {args.input_midi}")

    tool_dir = os.path.dirname(os.path.abspath(__file__))
    py = sys.executable

    cmds = [
        [
            py,
            os.path.join(tool_dir, "midi_to_domiso_dense3layer.py"),
            args.input_midi,
            "--out-dir",
            args.out_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_longnote.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_longnote_human.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_longnote_human_v2.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_restore.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_literal.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_literal_melodylock.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_yihuan_melodylock.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_yihuan_restore36.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_yihuan_noki_like.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_yihuan_midlead36.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_yihuan_ballad36.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_yihuan_lowlead36.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_sky_melodylock.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_sky_duet.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_sky_melodylock_human.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_sky_literal.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_literal_transcription.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_literal_human.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_horn_literal.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_guitar_literal.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_literal_arranged.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_guitar.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_horn.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
        [
            py,
            os.path.join(tool_dir, "domiso_pipeline_highlight.py"),
            "pipeline",
            args.input_midi,
            "--profile",
            "auto",
            "--out-dir",
            args.out_dir,
            "--report-dir",
            args.report_dir,
        ],
    ]

    for i, cmd in enumerate(cmds, start=1):
        print(f"[{i}/{len(cmds)}] {' '.join(cmd)}")
        out = run_cmd(cmd)
        print((out or "").strip())


if __name__ == "__main__":
    main()
