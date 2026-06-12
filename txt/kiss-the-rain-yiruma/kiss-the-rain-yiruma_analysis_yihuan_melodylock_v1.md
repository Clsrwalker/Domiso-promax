# Analysis (Yihuan 36-Key MelodyLock Script): kiss-the-rain-yiruma.mid

## Metrics
- note_count: 1052
- duration_s: 266.49997201074785
- tempo0: 63
- tempo_events: 8
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.701492537313433
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 33
- pitch_max: 97

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
- base_shift: -4
- dynamic_windows: w00-w03:-6, w04-w09:-4, w10-w16:-2
- lead_notes: 394
- lead_from_melody_track: 392 (99.5%)
- lead_from_top_note: 394 (100.0%)
- fallback_lead_notes: 2
- support_notes_pruned: 44
- chromatic_tokens: 439
