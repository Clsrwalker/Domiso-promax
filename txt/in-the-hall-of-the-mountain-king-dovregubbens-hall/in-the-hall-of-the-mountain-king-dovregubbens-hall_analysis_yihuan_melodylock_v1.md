# Analysis (Yihuan 36-Key MelodyLock Script): in-the-hall-of-the-mountain-king-dovregubbens-hall.mid

## Metrics
- note_count: 1430
- duration_s: 143.00652173913042
- tempo0: 138
- tempo_events: 4
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 16.25
- bar_density_p90: 22.2
- tracks: 2
- pitch_min: 23
- pitch_max: 99

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
- base_shift: 7
- dynamic_windows: w00-w06:+10, w07-w11:+7, w12-w21:+5
- lead_notes: 560
- lead_from_melody_track: 516 (92.1%)
- lead_from_top_note: 560 (100.0%)
- fallback_lead_notes: 44
- support_notes_pruned: 100
- chromatic_tokens: 349
