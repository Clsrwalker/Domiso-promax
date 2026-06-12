# Analysis (Yihuan 36-Key MelodyLock Script): moonlight-sonata-3rd-movement.mid

## Metrics
- note_count: 6414
- duration_s: 374.8058823529412
- tempo0: 170
- tempo_events: 3
- time_sig: 4/4
- max_poly: 10
- bar_density_mean: 24.295454545454547
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 29
- pitch_max: 88

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
- dynamic_windows: w00-w36:+3, w37-w41:+7, w42-w65:+3
- lead_notes: 2385
- lead_from_melody_track: 2283 (95.7%)
- lead_from_top_note: 2385 (100.0%)
- fallback_lead_notes: 102
- support_notes_pruned: 1578
- chromatic_tokens: 1187
