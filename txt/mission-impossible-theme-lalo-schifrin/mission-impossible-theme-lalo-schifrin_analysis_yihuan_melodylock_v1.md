# Analysis (Yihuan 36-Key MelodyLock Script): mission-impossible-theme-lalo-schifrin.mid

## Metrics
- note_count: 2756
- duration_s: 193.805
- tempo0: 100
- tempo_events: 3
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 25.51851851851852
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 26
- pitch_max: 108

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
- base_shift: -1
- dynamic_windows: w00-w01:+2, w02-w06:-1, w07-w20:+1
- lead_notes: 838
- lead_from_melody_track: 824 (98.3%)
- lead_from_top_note: 791 (94.4%)
- fallback_lead_notes: 14
- support_notes_pruned: 198
- chromatic_tokens: 1161
