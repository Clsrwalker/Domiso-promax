from __future__ import annotations

import ctypes
import platform
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class WindowInfo:
    hwnd: int
    title: str


def _require_windows() -> None:
    if platform.system().lower() != "windows":
        raise RuntimeError("window focus control only works on Windows")


def list_windows(title_contains: str = "") -> List[WindowInfo]:
    _require_windows()
    user32 = ctypes.windll.user32
    needle = title_contains.lower()
    windows: List[WindowInfo] = []

    enum_proc_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def callback(hwnd, _lparam) -> bool:
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        title = buffer.value
        if title and (not needle or needle in title.lower()):
            windows.append(WindowInfo(int(hwnd), title))
        return True

    user32.EnumWindows(enum_proc_type(callback), 0)
    return windows


def activate_window(title_contains: str) -> WindowInfo:
    if not title_contains.strip():
        raise ValueError("window title match is empty")
    matches = list_windows(title_contains)
    if not matches:
        raise RuntimeError(f"target window not found: {title_contains}")
    target = matches[0]
    user32 = ctypes.windll.user32
    if user32.IsIconic(target.hwnd):
        user32.ShowWindow(target.hwnd, 9)
    user32.SetForegroundWindow(target.hwnd)
    return target
