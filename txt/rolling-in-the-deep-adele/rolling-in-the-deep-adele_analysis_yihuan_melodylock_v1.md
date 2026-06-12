# Analysis (Yihuan 36-Key MelodyLock Script): rolling-in-the-deep-adele.mid

## Metrics
- note_count: 1007
- duration_s: 127.09499999999998
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.0
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 43
- pitch_max: 86

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
- dynamic_windows: w00-w03:+7, w04-w09:+4, w10-w13:+1
- lead_notes: 321
- lead_from_melody_track: 298 (92.8%)
- lead_from_top_note: 319 (99.4%)
- fallback_lead_notes: 23
- support_notes_pruned: 51
- chromatic_tokens: 147
