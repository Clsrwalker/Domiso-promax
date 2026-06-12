from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class KeyStroke:
    key: str
    modifiers: Tuple[str, ...] = ()

    @classmethod
    def parse(cls, value: str) -> "KeyStroke":
        parts = [p.strip().lower() for p in value.replace(" ", "").split("+") if p.strip()]
        if not parts:
            raise ValueError("empty key stroke")
        mods = tuple(p for p in parts[:-1] if p in {"shift", "ctrl", "control", "alt"})
        normalized = tuple("ctrl" if p == "control" else p for p in mods)
        return cls(parts[-1], normalized)

    def display(self) -> str:
        return "+".join((*self.modifiers, self.key)) if self.modifiers else self.key


SKY15_MIDI_TO_KEY: Dict[int, str] = {
    60: "y",
    62: "u",
    64: "i",
    65: "o",
    67: "p",
    69: "h",
    71: "j",
    72: "k",
    74: "l",
    76: ";",
    77: "n",
    79: "m",
    81: ",",
    83: ".",
    84: "/",
}


DOMISO36_MIDI_TO_KEY: Dict[int, str] = {
    48: "z",
    50: "x",
    52: "c",
    53: "v",
    55: "b",
    57: "n",
    59: "m",
    60: "a",
    62: "s",
    64: "d",
    65: "f",
    67: "g",
    69: "h",
    71: "j",
    72: "q",
    74: "w",
    76: "e",
    77: "r",
    79: "t",
    81: "y",
    83: "u",
    49: "shift+z",
    51: "ctrl+c",
    54: "shift+v",
    56: "shift+b",
    58: "ctrl+m",
    61: "shift+a",
    63: "ctrl+d",
    66: "shift+f",
    68: "shift+g",
    70: "ctrl+j",
    73: "shift+q",
    75: "ctrl+e",
    78: "shift+r",
    80: "shift+t",
    82: "ctrl+u",
}


KEYMAPS: Dict[str, Dict[int, str]] = {
    "sky15": SKY15_MIDI_TO_KEY,
    "domiso36": DOMISO36_MIDI_TO_KEY,
}


def layout_names() -> Iterable[str]:
    return sorted(KEYMAPS)


def map_midi_to_key(midi_note: int, layout: str) -> str | None:
    return KEYMAPS.get(layout, {}).get(midi_note)
