# Analysis (Yihuan 36-Key MelodyLock Script): 将世事高枕.mid

## Metrics
- note_count: 679
- duration_s: 133.84855769230768
- tempo0: 104
- tempo_events: 2
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 11.912280701754385
- bar_density_p90: 17.4
- tracks: 2
- pitch_min: 37
- pitch_max: 87

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
- dynamic_windows: w00-w09:+8, w10-w14:+6
- lead_notes: 279
- lead_from_melody_track: 258 (92.5%)
- lead_from_top_note: 279 (100.0%)
- fallback_lead_notes: 21
- support_notes_pruned: 3
- chromatic_tokens: 338
