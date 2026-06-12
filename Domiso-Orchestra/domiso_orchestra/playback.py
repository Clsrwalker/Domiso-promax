from __future__ import annotations

import ctypes
import platform
import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Mapping, Tuple

from .keymaps import KeyStroke


class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [("ki", _KEYBDINPUT)]


class _INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("union", _INPUT_UNION)]


@dataclass(frozen=True)
class PlaybackAction:
    time_ms: int
    key: str
    down: bool


@dataclass(frozen=True)
class PlaybackProfile:
    speed_percent: float = 100.0
    hold_min_ms: int = 150
    same_key_min_gap_ms: int = 110
    tap_press_ms: int = 14
    long_note_release_early_ms: int = 80

    @classmethod
    def from_payload(cls, payload: object = None) -> "PlaybackProfile":
        if not isinstance(payload, Mapping):
            return cls()

        def number(name: str, default: float, low: float, high: float) -> float:
            try:
                value = float(payload.get(name, default))
            except (TypeError, ValueError):
                return default
            return value if low <= value <= high else default

        def integer(name: str, default: int, low: int, high: int) -> int:
            return int(round(number(name, float(default), float(low), float(high))))

        return cls(
            speed_percent=number("speedPercent", 100.0, 1.0, 300.0),
            hold_min_ms=integer("holdMinMs", 150, 1, 5000),
            same_key_min_gap_ms=integer("sameKeyMinGapMs", 110, 0, 5000),
            tap_press_ms=integer("tapPressMs", 14, 1, 1000),
            long_note_release_early_ms=integer("longNoteReleaseEarlyMs", 80, 0, 5000),
        )

    def to_dict(self) -> Dict[str, object]:
        return {
            "speedPercent": self.speed_percent,
            "holdMinMs": self.hold_min_ms,
            "sameKeyMinGapMs": self.same_key_min_gap_ms,
            "tapPressMs": self.tap_press_ms,
            "longNoteReleaseEarlyMs": self.long_note_release_early_ms,
        }

    @property
    def time_scale(self) -> float:
        return 100.0 / max(1.0, self.speed_percent)


@dataclass(frozen=True)
class _KeySpan:
    start_ms: int
    duration_ms: int
    key: str

    @property
    def end_ms(self) -> int:
        return self.start_ms + self.duration_ms


def _collect_spans(tracks: Iterable[Dict[str, object]], profile: PlaybackProfile) -> List[_KeySpan]:
    spans: List[_KeySpan] = []
    scale = profile.time_scale
    for track in tracks:
        for event in track.get("events", []):
            if not isinstance(event, dict):
                continue
            start = int(round(float(event.get("timeMs", 0)) * scale))
            duration = max(1, int(round(float(event.get("durationMs", 80)) * scale)))
            for key in event.get("keys", []):
                spans.append(_KeySpan(start, duration, str(key)))
    spans.sort(key=lambda s: (s.start_ms, s.key, s.duration_ms))
    return spans


def _merge_same_key_spans(spans: Iterable[_KeySpan], profile: PlaybackProfile) -> List[_KeySpan]:
    merged: List[_KeySpan] = []
    by_key: Dict[str, List[_KeySpan]] = {}
    for span in spans:
        by_key.setdefault(span.key, []).append(span)
    for key, key_spans in by_key.items():
        key_spans.sort(key=lambda s: (s.start_ms, s.duration_ms))
        current: _KeySpan | None = None
        for span in key_spans:
            if current is None:
                current = span
                continue
            starts_close = span.start_ms - current.start_ms < profile.same_key_min_gap_ms
            overlaps = span.start_ms <= current.end_ms
            if starts_close or overlaps:
                end_ms = max(current.end_ms, span.end_ms)
                current = _KeySpan(current.start_ms, max(1, end_ms - current.start_ms), key)
            else:
                merged.append(current)
                current = span
        if current is not None:
            merged.append(current)
    merged.sort(key=lambda s: (s.start_ms, s.key, s.duration_ms))
    return merged


def build_actions(
    tracks: Iterable[Dict[str, object]],
    profile: PlaybackProfile | Mapping[str, object] | None = None,
) -> List[PlaybackAction]:
    playback_profile = profile if isinstance(profile, PlaybackProfile) else PlaybackProfile.from_payload(profile)
    spans = _merge_same_key_spans(_collect_spans(tracks, playback_profile), playback_profile)
    actions: List[PlaybackAction] = []
    for span in spans:
        if span.duration_ms >= playback_profile.hold_min_ms:
            release_ms = span.start_ms + span.duration_ms - playback_profile.long_note_release_early_ms
        else:
            release_ms = span.start_ms + playback_profile.tap_press_ms
        release_ms = max(span.start_ms + 1, release_ms)
        actions.append(PlaybackAction(span.start_ms, span.key, True))
        actions.append(PlaybackAction(release_ms, span.key, False))
    actions.sort(key=lambda a: (a.time_ms, 0 if a.down else 1, a.key))
    return actions


def actions_duration_ms(actions: Iterable[PlaybackAction]) -> int:
    return max((action.time_ms for action in actions), default=0)


def slice_actions_from_position(actions: Iterable[PlaybackAction], position_ms: int) -> List[PlaybackAction]:
    ordered = sorted(actions, key=lambda a: (a.time_ms, 0 if a.down else 1, a.key))
    position = max(0, int(position_ms))
    if position <= 0:
        return list(ordered)

    active: Dict[str, bool] = {}
    boundary_keys = {action.key for action in ordered if action.time_ms == position}
    for action in ordered:
        if action.time_ms >= position:
            break
        active[action.key] = action.down

    sliced: List[PlaybackAction] = [
        PlaybackAction(0, key, True)
        for key, is_down in sorted(active.items())
        if is_down and key not in boundary_keys
    ]
    sliced.extend(
        PlaybackAction(action.time_ms - position, action.key, action.down)
        for action in ordered
        if action.time_ms >= position
    )
    sliced.sort(key=lambda a: (a.time_ms, 0 if a.down else 1, a.key))
    return sliced


class KeyBackend:
    def key_down(self, key: str) -> None:
        raise NotImplementedError

    def key_up(self, key: str) -> None:
        raise NotImplementedError

    def release_all(self) -> None:
        pass


class DryRunBackend(KeyBackend):
    def __init__(self, echo: bool = False) -> None:
        self.echo = echo
        self.actions: List[Tuple[str, str]] = []

    def key_down(self, key: str) -> None:
        self.actions.append(("down", key))
        if self.echo:
            print(f"DOWN {key}")

    def key_up(self, key: str) -> None:
        self.actions.append(("up", key))
        if self.echo:
            print(f"UP   {key}")


class WindowsSendInputBackend(KeyBackend):
    VK: Dict[str, int] = {
        **{chr(i + 97): 0x41 + i for i in range(26)},
        **{str(i): 0x30 + i for i in range(10)},
        ";": 0xBA,
        "=": 0xBB,
        ",": 0xBC,
        "-": 0xBD,
        ".": 0xBE,
        "/": 0xBF,
        "`": 0xC0,
        "[": 0xDB,
        "\\": 0xDC,
        "]": 0xDD,
        "'": 0xDE,
        "space": 0x20,
        "enter": 0x0D,
        "tab": 0x09,
        "esc": 0x1B,
    }
    MOD_VK = {"shift": 0x10, "ctrl": 0x11, "alt": 0x12}
    KEYEVENTF_KEYUP = 0x0002
    INPUT_KEYBOARD = 1

    def __init__(self) -> None:
        if platform.system().lower() != "windows":
            raise RuntimeError("WindowsSendInputBackend only works on Windows")
        self._active_keys: set[str] = set()
        self._lock = threading.Lock()

    def _vk_for(self, key: str) -> int:
        k = key.lower()
        if k not in self.VK:
            raise ValueError(f"Unsupported key: {key}")
        return self.VK[k]

    def _send_vk(self, vk: int, down: bool) -> None:
        flags = 0 if down else self.KEYEVENTF_KEYUP
        extra = ctypes.c_ulong(0)
        inp = _INPUT(
            type=self.INPUT_KEYBOARD,
            union=_INPUT_UNION(ki=_KEYBDINPUT(vk, 0, flags, 0, ctypes.pointer(extra))),
        )
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    def key_down(self, key: str) -> None:
        stroke = KeyStroke.parse(key)
        with self._lock:
            for mod in stroke.modifiers:
                self._send_vk(self.MOD_VK[mod], True)
            self._send_vk(self._vk_for(stroke.key), True)
            for mod in reversed(stroke.modifiers):
                self._send_vk(self.MOD_VK[mod], False)
            self._active_keys.add(stroke.key)

    def key_up(self, key: str) -> None:
        stroke = KeyStroke.parse(key)
        with self._lock:
            self._send_vk(self._vk_for(stroke.key), False)
            self._active_keys.discard(stroke.key)

    def release_all(self) -> None:
        with self._lock:
            for key in list(self._active_keys):
                try:
                    self._send_vk(self._vk_for(key), False)
                except Exception:
                    pass
            self._active_keys.clear()
            for mod in self.MOD_VK:
                try:
                    self._send_vk(self.MOD_VK[mod], False)
                except Exception:
                    pass


class WindowsKeybdEventBackend(WindowsSendInputBackend):
    KEYEVENTF_EXTENDEDKEY = 0x0001
    MAPVK_VK_TO_VSC = 0

    def _send_vk(self, vk: int, down: bool) -> None:
        flags = 0 if down else self.KEYEVENTF_KEYUP
        scan = ctypes.windll.user32.MapVirtualKeyW(vk, self.MAPVK_VK_TO_VSC)
        ctypes.windll.user32.keybd_event(vk, scan, flags, 0)


def make_backend(name: str) -> KeyBackend:
    if name == "dry-run":
        return DryRunBackend()
    if name in {"windows", "windows-event"}:
        return WindowsKeybdEventBackend()
    if name == "windows-input":
        return WindowsSendInputBackend()
    raise ValueError(f"Unknown playback backend: {name}")


class PlaybackEngine:
    def __init__(self, backend: KeyBackend, time_scale: float = 1.0) -> None:
        self.backend = backend
        self.time_scale = max(0.0, time_scale)
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()

    def stop(self) -> None:
        self.stop_event.set()
        self.pause_event.clear()
        self.backend.release_all()

    def pause(self) -> None:
        self.pause_event.set()
        self.backend.release_all()

    def resume(self) -> None:
        self.pause_event.clear()

    def play(
        self,
        actions: List[PlaybackAction],
        start_monotonic_ms: float,
        on_state: Callable[[str], None] | None = None,
        on_progress: Callable[[int, int], None] | None = None,
        position_offset_ms: int = 0,
        total_duration_ms: int | None = None,
    ) -> None:
        self.stop_event.clear()
        self.pause_event.clear()
        position_offset = max(0, int(position_offset_ms))
        action_total_ms = actions_duration_ms(actions)
        total_ms = max(position_offset + action_total_ms, int(total_duration_ms or 0))
        last_progress_emit = 0.0

        def emit_progress(local_position_ms: int, force: bool = False) -> None:
            nonlocal last_progress_emit
            now = time.monotonic() * 1000.0
            if force or now - last_progress_emit >= 250:
                last_progress_emit = now
                if on_progress:
                    position_ms = position_offset + local_position_ms
                    on_progress(max(0, min(total_ms, position_ms)), total_ms)

        def wait_until(target_ms: float, playback_start_ms: float, paused_ms: float) -> tuple[bool, float]:
            nonlocal last_progress_emit
            while not self.stop_event.is_set():
                if self.pause_event.is_set():
                    self.backend.release_all()
                    if on_state:
                        on_state("PAUSED")
                    pause_started = time.monotonic() * 1000.0
                    while self.pause_event.is_set() and not self.stop_event.is_set():
                        elapsed = int((pause_started - playback_start_ms - paused_ms) / max(self.time_scale, 0.000001))
                        emit_progress(elapsed)
                        time.sleep(0.05)
                    paused_ms += time.monotonic() * 1000.0 - pause_started
                    if self.stop_event.is_set():
                        return False, paused_ms
                    if on_state:
                        on_state("PLAYING")
                    target_ms += time.monotonic() * 1000.0 - pause_started
                remain = target_ms - time.monotonic() * 1000.0
                position_ms = int((time.monotonic() * 1000.0 - playback_start_ms - paused_ms) / max(self.time_scale, 0.000001))
                emit_progress(position_ms)
                if remain <= 0:
                    return True, paused_ms
                time.sleep(min(0.01, remain / 1000.0))
            return False, paused_ms

        try:
            now_ms = time.monotonic() * 1000.0
            if start_monotonic_ms > now_ms:
                if on_state:
                    on_state("ARMED")
                while not self.stop_event.is_set():
                    remain = start_monotonic_ms - time.monotonic() * 1000.0
                    if remain <= 0:
                        break
                    time.sleep(min(0.05, remain / 1000.0))
            if self.stop_event.is_set():
                return
            if on_state:
                on_state("PLAYING")
            real_start = time.monotonic() * 1000.0
            paused_total_ms = 0.0
            emit_progress(0, force=True)
            for action in actions:
                target = real_start + action.time_ms * self.time_scale + paused_total_ms
                ok, paused_total_ms = wait_until(target, real_start, paused_total_ms)
                if not ok:
                    break
                if action.down:
                    self.backend.key_down(action.key)
                else:
                    self.backend.key_up(action.key)
            if not self.stop_event.is_set():
                emit_progress(max(0, total_ms - position_offset), force=True)
            if on_state and not self.stop_event.is_set():
                on_state("FINISHED")
        finally:
            self.backend.release_all()
