from __future__ import annotations

import ctypes
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class WindowInfo:
    hwnd: int
    title: str
    process_name: str = ""


def _require_windows() -> None:
    if platform.system().lower() != "windows":
        raise RuntimeError("window focus control only works on Windows")


def _process_name_for_hwnd(hwnd: int) -> str:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if not pid.value:
        return ""
    handle = kernel32.OpenProcess(0x1000, False, pid.value)
    if not handle:
        return ""
    try:
        size = ctypes.c_ulong(32768)
        buffer = ctypes.create_unicode_buffer(size.value)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return Path(buffer.value).name
    finally:
        kernel32.CloseHandle(handle)
    return ""


def list_windows(title_contains: str = "", process_name: str = "") -> List[WindowInfo]:
    _require_windows()
    user32 = ctypes.windll.user32
    needle = title_contains.lower()
    process_needle = process_name.lower()
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
        proc_name = _process_name_for_hwnd(hwnd) if process_needle else ""
        title_matches = not needle or needle in title.lower()
        process_matches = not process_needle or proc_name.lower() == process_needle
        if title and title_matches and process_matches:
            windows.append(WindowInfo(int(hwnd), title, proc_name))
        return True

    user32.EnumWindows(enum_proc_type(callback), 0)
    return windows


def activate_window(title_contains: str = "", process_name: str = "") -> WindowInfo:
    if not title_contains.strip() and not process_name.strip():
        raise ValueError("window title/process match is empty")
    matches = list_windows(title_contains, process_name)
    if not matches:
        target = process_name or title_contains
        raise RuntimeError(f"target window not found: {target}")
    target = matches[0]
    user32 = ctypes.windll.user32
    if user32.IsIconic(target.hwnd):
        user32.ShowWindow(target.hwnd, 9)
    user32.SetForegroundWindow(target.hwnd)
    return target
