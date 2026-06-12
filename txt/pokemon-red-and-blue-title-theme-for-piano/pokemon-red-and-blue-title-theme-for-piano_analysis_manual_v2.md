# Analysis (Manual v2 Literal): pokemon-red-and-blue-title-theme-for-piano.mid

## Manual Objective
- maximize one-to-one recognizability
- avoid de-clutter and arrangement-style thinning
- preserve section rhythm and phrase density from source MIDI

## Strategy
- base: `domiso_script_literal_v2` (literal_strict)
- fixed transpose across whole piece (`w00-w08:+12`) to avoid section color drift
- high/mid/low simultaneous notes distributed to A/B/C without intentional note deletion

## Limitation (Platform)
- DoMiSo 21-key mapping forces non-white notes to nearest playable tones
- this remains the main unavoidable source of difference from original MIDI timbre/pitch detail
