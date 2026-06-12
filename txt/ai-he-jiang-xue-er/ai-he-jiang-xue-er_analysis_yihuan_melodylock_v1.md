# Analysis (Yihuan 36-Key MelodyLock Script): ai-he-jiang-xue-er.mid

## Metrics
- note_count: 1017
- duration_s: 220.0
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.646153846153846
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 39
- pitch_max: 83

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
- base_shift: 8
- dynamic_windows: w00-w10:+8, w11-w12:+5, w13-w16:+8
- lead_notes: 483
- lead_from_melody_track: 476 (98.6%)
- lead_from_top_note: 483 (100.0%)
- fallback_lead_notes: 7
- support_notes_pruned: 0
- chromatic_tokens: 140
