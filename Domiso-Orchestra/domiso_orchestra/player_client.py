from __future__ import annotations

import argparse
import asyncio
import json
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

import websockets

from .client_config import default_config_path, load_client_config, save_client_config
from .playback import (
    DryRunBackend,
    PlaybackAction,
    PlaybackEngine,
    PlaybackProfile,
    actions_duration_ms,
    build_actions,
    make_backend,
    slice_actions_from_position,
)
from .window_focus import activate_window, list_windows


def monotonic_ms() -> float:
    return time.monotonic() * 1000.0


class PlayerClient:
    def __init__(
        self,
        *,
        server: str,
        client_id: str,
        name: str,
        layout: str,
        backend_name: str,
        input_delay_offset_ms: int,
        auto_ready: bool,
        time_scale: float,
        playback_profile_override: Optional[PlaybackProfile],
        config_path: Optional[Path],
        save_config: bool,
        window_title: str,
        window_exe: str,
    ) -> None:
        self.server = server
        self.client_id = client_id
        self.name = name or client_id
        self.layout = layout
        self.backend_name = backend_name
        self.input_delay_offset_ms = input_delay_offset_ms
        self.auto_ready = auto_ready
        self.time_scale = time_scale
        self.playback_profile_override = playback_profile_override
        self.config_path = config_path
        self.save_config_enabled = save_config
        self.window_title = window_title
        self.window_exe = window_exe
        self.state = "DISCONNECTED"
        self.loaded_project: Optional[Dict[str, object]] = None
        self.loaded_tracks: List[str] = []
        self.clock_offset_ms = 0.0
        self.best_rtt_ms = float("inf")
        self.last_rtt_ms = 0.0
        self.progress_ms = 0
        self.duration_ms = 0
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.engine = PlaybackEngine(make_backend(backend_name), time_scale=time_scale)
        self.play_thread: Optional[threading.Thread] = None
        self.persist_config()

    def persist_config(self) -> None:
        if not self.save_config_enabled or not self.config_path:
            return
        save_client_config(
            self.config_path,
            {
                "clientId": self.client_id,
                "name": self.name,
                "layout": self.layout,
                "backend": self.backend_name,
                "inputDelayOffsetMs": self.input_delay_offset_ms,
                "manualReady": not self.auto_ready,
                "windowTitle": self.window_title,
                "windowExe": self.window_exe,
            },
        )

    async def ensure_target_window(self) -> bool:
        if self.backend_name == "dry-run" or (not self.window_title.strip() and not self.window_exe.strip()):
            return True
        try:
            target = activate_window(self.window_title, self.window_exe)
            process = f" ({target.process_name})" if target.process_name else ""
            print(f"Activated target window: {target.title}{process}")
            return True
        except Exception as exc:
            await self.send_state("ERROR", f"target window focus failed: {exc}")
            return False

    async def send_state(self, state: Optional[str] = None, error: str = "") -> None:
        if state:
            self.state = state
        if not self.ws:
            return
        await self.ws.send(
            json.dumps(
                {
                    "type": "STATE",
                    "state": self.state,
                    "loadedTracks": self.loaded_tracks,
                    "inputDelayOffsetMs": self.input_delay_offset_ms,
                    "syncRttMs": round(self.last_rtt_ms, 2),
                    "bestSyncRttMs": round(self.best_rtt_ms, 2) if self.best_rtt_ms != float("inf") else 0,
                    "clockOffsetMs": round(self.clock_offset_ms, 2),
                    "progressMs": self.progress_ms,
                    "durationMs": self.duration_ms,
                    "windowTitle": self.window_title,
                    "windowExe": self.window_exe,
                    "error": error,
                },
                ensure_ascii=False,
            )
        )

    async def sync_loop(self) -> None:
        while self.ws:
            try:
                await self.ws.send(
                    json.dumps(
                        {
                            "type": "SYNC_REQUEST",
                            "clientSentMonotonicMs": monotonic_ms(),
                        }
                    )
                )
                await asyncio.sleep(1.0)
            except Exception:
                return

    def _state_callback(self, loop: asyncio.AbstractEventLoop, state: str) -> None:
        asyncio.run_coroutine_threadsafe(self.send_state(state), loop)

    def _progress_callback(self, loop: asyncio.AbstractEventLoop, progress_ms: int, duration_ms: int) -> None:
        self.progress_ms = progress_ms
        self.duration_ms = duration_ms
        asyncio.run_coroutine_threadsafe(self.send_state(), loop)

    def _play_on_thread(
        self,
        loop: asyncio.AbstractEventLoop,
        actions: List[PlaybackAction],
        start_monotonic_ms: float,
        position_offset_ms: int = 0,
        total_duration_ms: int | None = None,
    ) -> None:
        try:
            self.engine.play(
                actions,
                start_monotonic_ms,
                lambda s: self._state_callback(loop, s),
                lambda p, d: self._progress_callback(loop, p, d),
                position_offset_ms,
                total_duration_ms,
            )
        except Exception as exc:
            asyncio.run_coroutine_threadsafe(self.send_state("ERROR", f"playback failed: {exc}"), loop)

    async def handle_load_project(self, msg: Dict[str, object]) -> None:
        project = msg.get("project")
        if not isinstance(project, dict):
            await self.send_state("ERROR", "LOAD_PROJECT missing project")
            return
        tracks = project.get("tracks") or []
        if not isinstance(tracks, list):
            await self.send_state("ERROR", "project.tracks is not a list")
            return
        self.loaded_project = project
        self.loaded_tracks = [str(t.get("id")) for t in tracks if isinstance(t, dict)]
        self.progress_ms = 0
        self.duration_ms = 0
        await self.send_state("LOADED")
        if self.auto_ready:
            await self.send_state("READY")

    async def handle_start(self, msg: Dict[str, object]) -> None:
        if not self.loaded_project:
            await self.send_state("ERROR", "START received before project load")
            return
        command_song_id = str(msg.get("songId") or "")
        loaded_song_id = str(self.loaded_project.get("songId") or "")
        if command_song_id and loaded_song_id and command_song_id != loaded_song_id:
            await self.send_state("ERROR", f"START songId mismatch: {command_song_id} != {loaded_song_id}")
            return
        tracks = self.loaded_project.get("tracks") or []
        project_profile = self.loaded_project.get("playbackProfile")
        playback_profile = self.playback_profile_override or PlaybackProfile.from_payload(project_profile)
        all_actions = build_actions((t for t in tracks if isinstance(t, dict)), playback_profile)
        total_duration_ms = actions_duration_ms(all_actions)
        start_position_ms = max(0, min(total_duration_ms, int(msg.get("startPositionMs") or 0)))
        actions = slice_actions_from_position(all_actions, start_position_ms)
        self.progress_ms = start_position_ms
        self.duration_ms = total_duration_ms
        start_at_server = float(msg.get("startAtServerTimeMs") or 0)
        local_start = start_at_server + self.input_delay_offset_ms - self.clock_offset_ms
        if not await self.ensure_target_window():
            return
        loop = asyncio.get_running_loop()
        self.engine.stop()
        self.play_thread = threading.Thread(
            target=self._play_on_thread,
            args=(
                loop,
                actions,
                local_start,
                start_position_ms,
                total_duration_ms,
            ),
            daemon=True,
        )
        self.play_thread.start()
        await self.send_state("ARMED")

    async def handle_test_pulse(self, msg: Dict[str, object]) -> None:
        keys = msg.get("keys") or ["y"]
        if not isinstance(keys, list) or not keys:
            await self.send_state("ERROR", "TEST_PULSE keys must be a non-empty list")
            return
        count = max(1, min(8, int(msg.get("count") or 3)))
        interval_ms = max(100, min(3000, int(msg.get("intervalMs") or 500)))
        press_ms = max(10, min(500, int(msg.get("pressMs") or 80)))
        actions: List[PlaybackAction] = []
        for index in range(count):
            start = index * interval_ms
            for key in keys:
                key_text = str(key)
                actions.append(PlaybackAction(start, key_text, True))
                actions.append(PlaybackAction(start + press_ms, key_text, False))
        actions.sort(key=lambda action: (action.time_ms, 0 if action.down else 1, action.key))
        self.progress_ms = 0
        self.duration_ms = actions_duration_ms(actions)
        if not await self.ensure_target_window():
            return
        loop = asyncio.get_running_loop()
        self.engine.stop()
        self.play_thread = threading.Thread(
            target=self._play_on_thread,
            args=(
                loop,
                actions,
                monotonic_ms() + 250,
            ),
            daemon=True,
        )
        self.play_thread.start()
        await self.send_state("ARMED")

    async def handle_message(self, msg: Dict[str, object]) -> None:
        msg_type = msg.get("type")
        if msg_type == "WELCOME":
            await self.send_state("CONNECTED")
        elif msg_type == "SYNC_ACK":
            sent = float(msg.get("clientSentMonotonicMs") or 0)
            now = monotonic_ms()
            rtt = max(0.0, now - sent)
            offset = float(msg.get("serverTimeMs") or 0) - (sent + rtt / 2.0)
            self.last_rtt_ms = rtt
            if rtt <= self.best_rtt_ms or self.best_rtt_ms == float("inf"):
                self.best_rtt_ms = rtt
                self.clock_offset_ms = offset
            await self.send_state()
        elif msg_type == "LOAD_PROJECT":
            await self.handle_load_project(msg)
        elif msg_type == "SET_READY":
            await self.send_state("READY")
        elif msg_type == "SET_DELAY":
            self.input_delay_offset_ms = int(msg.get("inputDelayOffsetMs") or 0)
            self.persist_config()
            await self.send_state(self.state)
        elif msg_type == "START":
            await self.handle_start(msg)
        elif msg_type == "TEST_PULSE":
            await self.handle_test_pulse(msg)
        elif msg_type == "PAUSE":
            self.engine.pause()
            await self.send_state("PAUSED")
        elif msg_type == "RESUME":
            self.engine.resume()
            await self.send_state("PLAYING")
        elif msg_type == "STOP":
            self.engine.stop()
            self.progress_ms = 0
            await self.send_state("LOADED" if self.loaded_project else "CONNECTED")
        elif msg_type == "ERROR":
            await self.send_state("ERROR", str(msg.get("error") or "server error"))

    async def run(self) -> None:
        while True:
            try:
                async with websockets.connect(self.server) as ws:
                    self.ws = ws
                    await ws.send(
                        json.dumps(
                            {
                                "type": "HELLO",
                                "clientId": self.client_id,
                                "name": self.name,
                                "layout": self.layout,
                                "inputDelayOffsetMs": self.input_delay_offset_ms,
                                "windowTitle": self.window_title,
                                "windowExe": self.window_exe,
                            },
                            ensure_ascii=False,
                        )
                    )
                    sync_task = asyncio.create_task(self.sync_loop())
                    try:
                        async for raw in ws:
                            await self.handle_message(json.loads(raw))
                    finally:
                        sync_task.cancel()
            except KeyboardInterrupt:
                self.engine.stop()
                raise
            except Exception as exc:
                self.ws = None
                self.state = "DISCONNECTED"
                print(f"Disconnected: {exc}. Reconnecting in 2s...")
                await asyncio.sleep(2.0)


def main() -> None:
    ap = argparse.ArgumentParser(description="Run a Domiso Orchestra Player Client.")
    ap.add_argument("--server", default="ws://127.0.0.1:8765/ws/player")
    ap.add_argument("--client-id", default="")
    ap.add_argument("--name", default="")
    ap.add_argument("--layout", default="")
    ap.add_argument("--backend", choices=["dry-run", "windows", "windows-event", "windows-input", "ahk"], default="")
    ap.add_argument("--delay-offset-ms", type=int, default=None)
    ap.add_argument("--manual-ready", action="store_true")
    ap.add_argument("--config", default="")
    ap.add_argument("--no-save-config", action="store_true")
    ap.add_argument("--window-title", default="")
    ap.add_argument("--window-exe", default="")
    ap.add_argument("--list-windows", action="store_true")
    ap.add_argument("--local-pulse", action="store_true")
    ap.add_argument("--local-pulse-key", default="y")
    ap.add_argument("--time-scale", type=float, default=1.0)
    ap.add_argument("--speed-percent", type=float, default=None)
    ap.add_argument("--hold-min-ms", type=int, default=None)
    ap.add_argument("--same-key-min-gap-ms", type=int, default=None)
    ap.add_argument("--tap-press-ms", type=int, default=None)
    ap.add_argument("--release-early-ms", type=int, default=None)
    args = ap.parse_args()
    if args.list_windows:
        try:
            for window in list_windows(args.window_title, args.window_exe):
                process = f" [{window.process_name}]" if window.process_name else ""
                print(f"{window.hwnd}: {window.title}{process}")
        except Exception as exc:
            raise SystemExit(str(exc)) from exc
        return

    explicit_config = Path(args.config) if args.config else None
    loaded_config = load_client_config(explicit_config) if explicit_config else {}
    client_id = args.client_id or str(loaded_config.get("clientId") or "").strip()
    if not client_id:
        if args.local_pulse:
            client_id = "local-pulse"
        else:
            raise SystemExit("--client-id is required unless --config contains clientId")
    config_path = explicit_config or default_config_path(client_id)
    loaded_config = {**load_client_config(config_path), **loaded_config}

    def cfg_str(name: str, fallback: str) -> str:
        value = loaded_config.get(name)
        return str(value) if value not in {None, ""} else fallback

    def cfg_int(name: str, fallback: int) -> int:
        try:
            return int(loaded_config.get(name, fallback))
        except (TypeError, ValueError):
            return fallback

    override_payload = {
        "speedPercent": args.speed_percent,
        "holdMinMs": args.hold_min_ms,
        "sameKeyMinGapMs": args.same_key_min_gap_ms,
        "tapPressMs": args.tap_press_ms,
        "longNoteReleaseEarlyMs": args.release_early_ms,
    }
    override_payload = {k: v for k, v in override_payload.items() if v is not None}
    if args.local_pulse:
        try:
            if args.window_title:
                target = activate_window(args.window_title, args.window_exe)
                process = f" ({target.process_name})" if target.process_name else ""
                print(f"Activated target window: {target.title}{process}")
            elif args.window_exe:
                target = activate_window(process_name=args.window_exe)
                process = f" ({target.process_name})" if target.process_name else ""
                print(f"Activated target window: {target.title}{process}")
            backend = DryRunBackend(echo=True) if (args.backend or cfg_str("backend", "dry-run")) == "dry-run" else make_backend(args.backend or cfg_str("backend", "dry-run"))
            engine = PlaybackEngine(backend, time_scale=args.time_scale)
            key = args.local_pulse_key
            actions = []
            for index in range(3):
                start = index * 500
                actions.append(PlaybackAction(start, key, True))
                actions.append(PlaybackAction(start + 80, key, False))
            engine.play(actions, monotonic_ms() + 250, on_state=lambda state: print(state))
        except Exception as exc:
            raise SystemExit(str(exc)) from exc
        return

    client = PlayerClient(
        server=args.server,
        client_id=client_id,
        name=args.name or cfg_str("name", client_id),
        layout=args.layout or cfg_str("layout", "sky15"),
        backend_name=args.backend or cfg_str("backend", "dry-run"),
        input_delay_offset_ms=args.delay_offset_ms if args.delay_offset_ms is not None else cfg_int("inputDelayOffsetMs", 0),
        auto_ready=not (args.manual_ready or bool(loaded_config.get("manualReady", False))),
        time_scale=args.time_scale,
        playback_profile_override=PlaybackProfile.from_payload(override_payload) if override_payload else None,
        config_path=config_path,
        save_config=not args.no_save_config,
        window_title=args.window_title or cfg_str("windowTitle", ""),
        window_exe=args.window_exe or cfg_str("windowExe", ""),
    )
    asyncio.run(client.run())


if __name__ == "__main__":
    main()
