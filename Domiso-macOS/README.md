# Domiso-macOS

This is a native macOS shell for Domiso. It does not attempt to run or port
the original AutoHotkey application. Instead it reimplements the Domiso sheet
parser, playback controls, macOS keyboard event output, and a bridge to the
existing Python MIDI conversion tools.

## Scope

- Single Domiso macOS app.
- No Genshin, Sky, or other game-version UI.
- Reuses the Domiso numbered sheet rules documented in `../Domiso/SYNTAX.md`.
- Reuses `../tools/domiso_generate_select.py` for MIDI to TXT generation.
- Sends keyboard events through macOS Accessibility and Quartz `CGEvent`.

## Requirements

- macOS 13 or newer.
- Xcode command line tools or Xcode.
- Python 3 if MIDI conversion is used.
- Accessibility permission for the built app or terminal that launches it.

## Run From Source

```bash
cd Domiso-macOS
swift run DomisoMacOS
```

If you launch with `swift run`, grant Accessibility permission to the terminal
app running the command. A packaged app will need its own Accessibility
permission.

## Verify And Package

```bash
cd Domiso-macOS
bash scripts/verify-macos.sh
bash scripts/package-app.sh
open .build/Domiso-macOS.app
```

The package script creates a local unsigned app bundle at
`.build/Domiso-macOS.app`. For distribution outside your own machine, sign and
notarize that bundle with your Apple Developer identity.

## MIDI Conversion

The app locates conversion tools in this order:

1. `DOMISO_TOOLS_DIR`
2. `../tools` relative to the current working directory
3. `../../tools` relative to the current working directory

The current bridge calls:

```bash
python3 domiso_generate_select.py <midi> --target yihuan --out-dir <dir> --report-dir <dir>
```

The target remains `yihuan` because the existing conversion registry names the
36-key Domiso output that way. The macOS app presents it as Domiso only.

## Compatibility Notes

- `0` is treated as a rest in this implementation.
- Key output uses the current Domiso 36-key mapping from `../Domiso/DoMiSo.ahk`.
- Chords, tuplets, rollback, BPM, key control, duration marks, and arpeggio
  marks are implemented in `Sources/DomisoCore/DomisoSheetParser.swift`.
- The app cannot be verified or signed from this Windows workspace. Build and
  runtime testing must happen on macOS.
