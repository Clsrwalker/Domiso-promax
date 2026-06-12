# Analysis (Yihuan 36-Key MelodyLock Script): call-your-name-hiroyuki-sawano-call-your-name.mid

## Metrics
- note_count: 1556
- duration_s: 261.4931972789115
- tempo0: 70
- tempo_events: 4
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 20.473684210526315
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 23
- pitch_max: 85

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
- base_shift: 3
- dynamic_windows: w00-w09:+3, w10-w10:+6, w11-w18:+5
- lead_notes: 461
- lead_from_melody_track: 450 (97.6%)
- lead_from_top_note: 458 (99.3%)
- fallback_lead_notes: 11
- support_notes_pruned: 13
- chromatic_tokens: 108
