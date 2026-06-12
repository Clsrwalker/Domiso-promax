# Analysis (Yihuan 36-Key MelodyLock Script): hes-a-pirate.mid

## Metrics
- note_count: 1285
- duration_s: 78.52857504814025
- tempo0: 207
- tempo_events: 7
- time_sig: 6/8
- max_poly: 6
- bar_density_mean: 14.94186046511628
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 26
- pitch_max: 84

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
- dynamic_windows: w00-w03:+9, w04-w05:+4, w06-w15:+6
- lead_notes: 328
- lead_from_melody_track: 273 (83.2%)
- lead_from_top_note: 328 (100.0%)
- fallback_lead_notes: 55
- support_notes_pruned: 9
- chromatic_tokens: 568
