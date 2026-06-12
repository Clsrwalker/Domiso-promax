# Analysis (Yihuan 36-Key MelodyLock Script): liang-zhi-lao-hu-liang-zhi-lao-hu-public-domain.mid

## Metrics
- note_count: 481
- duration_s: 80.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 3
- bar_density_mean: 12.025
- bar_density_p90: 18.9
- tracks: 2
- pitch_min: 36
- pitch_max: 81

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
- base_shift: 4
- dynamic_windows: w00-w05:+6, w06-w07:+2, w08-w09:+6
- lead_notes: 240
- lead_from_melody_track: 240 (100.0%)
- lead_from_top_note: 240 (100.0%)
- fallback_lead_notes: 0
- support_notes_pruned: 10
- chromatic_tokens: 302
