# Analysis (Yihuan 36-Key MelodyLock Script): nod-krai.mid

## Metrics
- note_count: 2539
- duration_s: 254.90157128257536
- tempo0: 76
- tempo_events: 2
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 24.650485436893202
- bar_density_p90: 38.0
- tracks: 2
- pitch_min: 21
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
- base_shift: 2
- dynamic_windows: w00-w03:-1, w04-w18:+5, w19-w25:+2
- lead_notes: 713
- lead_from_melody_track: 707 (99.2%)
- lead_from_top_note: 696 (97.6%)
- fallback_lead_notes: 6
- support_notes_pruned: 216
- chromatic_tokens: 689
