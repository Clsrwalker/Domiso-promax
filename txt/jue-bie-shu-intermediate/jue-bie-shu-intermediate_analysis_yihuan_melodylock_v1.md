# Analysis (Yihuan 36-Key MelodyLock Script): jue-bie-shu-intermediate.mid

## Metrics
- note_count: 1607
- duration_s: 249.2121212121212
- tempo0: 90
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 14.87962962962963
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 26
- pitch_max: 98

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
- base_shift: 2
- dynamic_windows: w00-w06:-1, w07-w19:+2, w20-w26:-1
- lead_notes: 571
- lead_from_melody_track: 570 (99.8%)
- lead_from_top_note: 571 (100.0%)
- fallback_lead_notes: 1
- support_notes_pruned: 35
- chromatic_tokens: 533
