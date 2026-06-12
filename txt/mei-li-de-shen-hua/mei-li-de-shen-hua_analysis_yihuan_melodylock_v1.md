# Analysis (Yihuan 36-Key MelodyLock Script): mei-li-de-shen-hua.mid

## Metrics
- note_count: 1820
- duration_s: 314.0
- tempo0: 60
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 23.636363636363637
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 29
- pitch_max: 94

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
- base_shift: 9
- dynamic_windows: w00-w02:+6, w03-w19:+9
- lead_notes: 471
- lead_from_melody_track: 462 (98.1%)
- lead_from_top_note: 469 (99.6%)
- fallback_lead_notes: 9
- support_notes_pruned: 137
- chromatic_tokens: 224
