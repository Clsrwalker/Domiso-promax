# Analysis (Yihuan 36-Key MelodyLock Script): poesy-of-chrysolite.mid

## Metrics
- note_count: 1163
- duration_s: 139.41195568280182
- tempo0: 94
- tempo_events: 11
- time_sig: 1/8
- max_poly: 7
- bar_density_mean: 2.60762331838565
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 31
- pitch_max: 91

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
- base_shift: -2
- dynamic_windows: w00-w00:+1, w01-w04:-3, w05-w13:+0
- lead_notes: 326
- lead_from_melody_track: 274 (84.0%)
- lead_from_top_note: 326 (100.0%)
- fallback_lead_notes: 52
- support_notes_pruned: 44
- chromatic_tokens: 437
