# DoMiSo Yihuan

This folder is a Neverness To Everness focused DoMiSo fork. It keeps the newer playback controls and UI workflow while switching the target game and keyboard model.

## Target
- Game: `Neverness To Everness`
- Main process: `HTGame.exe`
- Fallback process: `NTEGame.exe`
- Game folder: `D:\Neverness To Everness`
- Project folder: `D:\domiso\DoMiSo-yihuan`

## What Changed
- Rebranded the app to Yihuan / Neverness To Everness.
- Switched process detection to `HTGame.exe`, with `NTEGame.exe` as a fallback.
- Kept the newer playback features: progress slider, pause/resume from paused position, and playback hotkeys.
- Switched the playable keyboard model to Yihuan's 36-key piano: 21 natural notes plus 15 semitone notes.
- Kept standard DoMiSo accidental syntax: `#` for sharp and `b` for flat, for example `1#`, `3b`, `+5#`.
- Updated the main UI palette to a warm Yihuan-specific style.
- Updated the tray menu to open the Yihuan game folder.

## Usage
1. Start `Neverness To Everness` and enter the piano UI.
2. Open `DoMiSo.ahk` or the compiled executable.
3. Paste a DoMiSo score, or use `File` to open a `txt` / `dms` file.
4. Use `Listen` for MIDI preview.
5. Use `Play` to auto-play into the game.
6. Hotkeys: `F7` pause, `F8` stop/reset, `F9` start from beginning, `F10` resume from paused position.

## Yihuan 36-Key Layout
- Natural-note rows:
  - High octave: `Q W E R T Y U`
  - Middle octave: `A S D F G H J`
  - Low octave: `Z X C V B N M`
- Semitone rule:
  - `Shift + key` plays the higher semitone shown by the game UI.
  - `Ctrl + key` plays the lower semitone shown by the game UI.
- DoMiSo note range supported by this app is MIDI `48-83`, equivalent to `-1` through `+7` with accidentals inside the three octaves.

## Notes
- This copy is intended as a local customized fork.
- Auto-update is disabled to avoid pulling releases from the original Genshin project.
- For semitone-heavy scores, use the Yihuan-compatible generator or write DoMiSo accidentals directly.

