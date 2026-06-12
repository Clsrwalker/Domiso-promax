from __future__ import annotations

import base64
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from domiso_orchestra.domiso_sheet import encrypt_dms_bytes


ROOT = Path(__file__).resolve().parent
PORT = 8876
BASE_URL = f"http://127.0.0.1:{PORT}"
WS_URL = f"ws://127.0.0.1:{PORT}/ws/player"


def vlq(value: int) -> bytes:
    parts = [value & 0x7F]
    value >>= 7
    while value:
        parts.append(0x80 | (value & 0x7F))
        value >>= 7
    return bytes(reversed(parts))


def midi_track(events: bytes) -> bytes:
    return b"MTrk" + len(events).to_bytes(4, "big") + events


def minimal_midi() -> bytes:
    header = b"MThd" + (6).to_bytes(4, "big") + (1).to_bytes(2, "big") + (2).to_bytes(2, "big") + (480).to_bytes(2, "big")
    tempo = b"\x00\xff\x03\x05Tempo\x00\xff\x51\x03\x07\xa1\x20\x00\xff\x2f\x00"
    melody = (
        b"\x00\xff\x03\x06Melody"
        + b"\x00\x90\x3c\x40"
        + vlq(480)
        + b"\x80\x3c\x00"
        + b"\x00\x90\x40\x40"
        + vlq(480)
        + b"\x80\x40\x00"
        + b"\x00\xff\x2f\x00"
    )
    return header + midi_track(tempo) + midi_track(melody)


def request_json(path: str, payload: dict | None = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE_URL + path, data=data, headers=headers, method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wait_for(predicate, timeout_s: float, label: str):
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        try:
            last = request_json("/api/state")
            if predicate(last):
                return last
        except (OSError, urllib.error.URLError):
            pass
        time.sleep(0.1)
    raise RuntimeError(f"timeout waiting for {label}; last={last}")


def start_process(args: list[str]) -> subprocess.Popen:
    return subprocess.Popen(
        args,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def main() -> None:
    procs: list[tuple[str, subprocess.Popen]] = []
    try:
        server = start_process(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "domiso_orchestra.conductor:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(PORT),
                "--no-access-log",
            ]
        )
        procs.append(("server", server))
        wait_for(lambda _: True, 10, "server")

        client_ids = ("PC-A", "PC-B", "PC-C")
        for client_id in client_ids:
            client_args = [
                sys.executable,
                "-m",
                "domiso_orchestra.player_client",
                "--server",
                WS_URL,
                "--client-id",
                client_id,
                "--backend",
                "dry-run",
                "--no-save-config",
                "--time-scale",
                "0.05",
            ]
            if client_id == "PC-C":
                client_args.append("--manual-ready")
            procs.append(
                (
                    client_id,
                    start_process(client_args),
                )
            )

        wait_for(lambda s: len(s.get("clients", [])) == 3, 10, "three clients")

        request_json("/api/client/PC-A/test", {"keys": ["y"], "count": 2, "intervalMs": 150, "pressMs": 30})
        wait_for(lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["state"] == "FINISHED", 10, "test pulse")

        midi_imported = request_json(
            "/api/project/midi",
            {
                "songId": "smoke_midi",
                "title": "Smoke MIDI",
                "layout": "domiso36",
                "contentBase64": base64.b64encode(minimal_midi()).decode("ascii"),
            },
        )
        if midi_imported.get("project", {}).get("tracks") != 1:
            raise RuntimeError(f"MIDI import failed: {midi_imported}")
        current = request_json("/api/project/current")
        if current.get("songId") != "smoke_midi":
            raise RuntimeError(f"current project export failed: {current.get('songId')}")

        imported = request_json(
            "/api/project/domiso",
            {
                "songId": "smoke_domiso",
                "title": "Smoke Domiso Import",
                "layout": "sky15",
                "playbackProfile": {
                    "speedPercent": 95,
                    "holdMinMs": 150,
                    "sameKeyMinGapMs": 110,
                    "tapPressMs": 14,
                    "longNoteReleaseEarlyMs": 80,
                },
                "tracks": [
                    {"id": "track_1", "name": "A", "text": "bpm=120\n1 2 3 4\n"},
                    {"id": "track_2", "name": "B", "text": "bpm=120\n( 1 3 5 )--\n"},
                    {
                        "id": "track_3",
                        "name": "C",
                        "fileName": "C.dms",
                        "contentBase64": base64.b64encode(
                            encrypt_dms_bytes("Title: C", "bpm=120\n{ 1 2 3 4 }\n")
                        ).decode("ascii"),
                    },
                ],
            },
        )
        if imported.get("project", {}).get("tracks") != 3:
            raise RuntimeError(f"Domiso import failed: {imported}")

        project = json.loads((ROOT / "samples" / "two_track.project.json").read_text(encoding="utf-8"))
        project["tracks"].extend(
            [
                {
                    "id": "track_3",
                    "name": "Rhythm",
                    "layout": "sky15",
                    "events": [
                        {"timeMs": 0, "durationMs": 120, "keys": ["n"]},
                        {"timeMs": 500, "durationMs": 120, "keys": ["m"]},
                    ],
                },
                {
                    "id": "track_4",
                    "name": "Second Voice",
                    "layout": "sky15",
                    "events": [
                        {"timeMs": 250, "durationMs": 180, "keys": ["k"]},
                        {"timeMs": 750, "durationMs": 180, "keys": ["l"]},
                    ],
                },
            ]
        )
        request_json("/api/project", project)
        request_json("/api/assign", {"trackId": "track_1", "clientId": "PC-A"})
        request_json("/api/assign", {"trackId": "track_2", "clientId": "PC-B"})
        request_json("/api/assign", {"trackId": "track_3", "clientId": "PC-C"})
        request_json("/api/assign", {"trackId": "track_4", "clientId": "PC-A"})
        request_json("/api/prepare", {})
        wait_for(
            lambda s: {c["client_id"]: c["state"] for c in s["clients"]} == {"PC-A": "READY", "PC-B": "READY", "PC-C": "LOADED"},
            10,
            "loaded/manual ready",
        )
        request_json("/api/client/PC-C/ready", {})
        wait_for(lambda s: {c["client_id"]: c["state"] for c in s["clients"]} == {"PC-A": "READY", "PC-B": "READY", "PC-C": "READY"}, 10, "ready")
        state = request_json("/api/state")
        tracks_by_client = {c["client_id"]: set(c.get("loaded_tracks", [])) for c in state["clients"]}
        if tracks_by_client.get("PC-A") != {"track_1", "track_4"}:
            raise RuntimeError(f"PC-A did not receive multiple tracks: {tracks_by_client}")
        start_info = request_json("/api/start", {"delayMs": 500})
        countdown_state = request_json("/api/state")
        if countdown_state.get("roomState") != "ARMED":
            raise RuntimeError(f"room did not enter ARMED: {countdown_state.get('roomState')}")
        if countdown_state.get("scheduledStartAtServerTimeMs") != start_info.get("startAtServerTimeMs"):
            raise RuntimeError(f"scheduled start mismatch: {countdown_state} vs {start_info}")
        wait_for(
            lambda s: {c["client_id"]: c["state"] for c in s["clients"]} == {"PC-A": "FINISHED", "PC-B": "FINISHED", "PC-C": "FINISHED"},
            10,
            "finished",
        )

        pause_project = {
            "schemaVersion": "domiso-orchestra.project.v1",
            "songId": "pause_smoke",
            "title": "Pause Smoke",
            "playbackProfile": {
                "speedPercent": 100,
                "holdMinMs": 150,
                "sameKeyMinGapMs": 110,
                "tapPressMs": 14,
                "longNoteReleaseEarlyMs": 80,
            },
            "tracks": [
                {
                    "id": "track_1",
                    "name": "Long",
                    "layout": "sky15",
                    "events": [{"timeMs": 0, "durationMs": 30000, "keys": ["y"]}],
                }
            ],
        }
        request_json("/api/project", pause_project)
        request_json("/api/assign", {"trackId": "track_1", "clientId": "PC-A"})
        request_json("/api/prepare", {})
        wait_for(lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["state"] == "READY", 10, "pause ready")
        request_json("/api/start", {"delayMs": 100})
        wait_for(lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["state"] == "PLAYING", 10, "pause playing")
        request_json("/api/pause", {})
        wait_for(lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["state"] == "PAUSED", 10, "paused")
        request_json("/api/resume", {})
        wait_for(lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["state"] == "FINISHED", 10, "pause finished")
        request_json("/api/prepare", {})
        wait_for(lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["state"] == "READY", 10, "seek ready")
        seek_start = request_json("/api/start", {"delayMs": 100, "startPositionMs": 10000})
        if seek_start.get("startPositionMs") != 10000:
            raise RuntimeError(f"seek start was not accepted: {seek_start}")
        wait_for(
            lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["progressMs"] >= 10000,
            10,
            "seek progress",
        )
        wait_for(lambda s: next(c for c in s["clients"] if c["client_id"] == "PC-A")["state"] == "FINISHED", 10, "seek finished")
        print("SMOKE_OK")
    finally:
        for _, proc in reversed(procs):
            if proc.poll() is None:
                proc.terminate()
        for _, proc in reversed(procs):
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        for name, proc in procs:
            try:
                out = proc.stdout.read() if proc.stdout else ""
            except Exception:
                out = ""
            if out.strip():
                print(f"--- {name} output ---")
                print(out.strip())


if __name__ == "__main__":
    main()
