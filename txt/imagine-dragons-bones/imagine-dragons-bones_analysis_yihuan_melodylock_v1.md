# Analysis (Yihuan 36-Key MelodyLock Script): imagine-dragons-bones.mid

## Metrics
- note_count: 1749
- duration_s: 158.94627192982458
- tempo0: 57
- tempo_events: 3
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 23.635135135135137
- bar_density_p90: 35.0
- tracks: 2
- pitch_min: 22
- pitch_max: 89

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
- base_shift: 6
- dynamic_windows: w00-w09:+6, w10-w13:+9, w14-w18:+8
- lead_notes: 492
- lead_from_melody_track: 481 (97.8%)
- lead_from_top_note: 492 (100.0%)
- fallback_lead_notes: 11
- support_notes_pruned: 68
- chromatic_tokens: 344
