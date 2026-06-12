# Analysis (Yihuan 36-Key MelodyLock Script): luv-letter.mid

## Metrics
- note_count: 1921
- duration_s: 295.4516979600596
- tempo0: 80
- tempo_events: 15
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.404040404040405
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 34
- pitch_max: 101

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
- base_shift: -6
- dynamic_windows: w00-w23:-6, w24-w24:-3
- lead_notes: 927
- lead_from_melody_track: 907 (97.8%)
- lead_from_top_note: 925 (99.8%)
- fallback_lead_notes: 20
- support_notes_pruned: 62
- chromatic_tokens: 213
