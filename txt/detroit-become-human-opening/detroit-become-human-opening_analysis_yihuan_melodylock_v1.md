# Analysis (Yihuan 36-Key MelodyLock Script): detroit-become-human-opening.mid

## Metrics
- note_count: 586
- duration_s: 100.00208333333333
- tempo0: 60
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.44
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 36
- pitch_max: 88

## Recommended Profile
- yihuan_melodylock_dense
- reason: dense piano texture -> yihuan_melodylock_dense

## Yihuan 36-Key MelodyLock Intent
- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- avoid turning sustained melody into stacked lead chords
- keep support notes in B/C instead of letting A absorb the whole piano texture
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 5
- dynamic_windows: w00-w00:+8, w01-w06:+5
- lead_notes: 238
- lead_from_melody_track: 232 (97.5%)
- lead_from_top_note: 238 (100.0%)
- fallback_lead_notes: 6
- support_notes_pruned: 163
- chromatic_tokens: 34
