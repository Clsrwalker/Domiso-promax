# Analysis (Yihuan 36-Key MelodyLock Script): aizo-king-gnu.mid

## Metrics
- note_count: 1237
- duration_s: 86.84210526315789
- tempo0: 190
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.92753623188406
- bar_density_p90: 25.0
- tracks: 2
- pitch_min: 33
- pitch_max: 100

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
- base_shift: -5
- dynamic_windows: w00-w01:-4, w02-w17:-5
- lead_notes: 465
- lead_from_melody_track: 444 (95.5%)
- lead_from_top_note: 465 (100.0%)
- fallback_lead_notes: 21
- support_notes_pruned: 35
- chromatic_tokens: 145
