# Analysis (Yihuan 36-Key MelodyLock Script): my-war-attack-on-titan.mid

## Metrics
- note_count: 963
- duration_s: 86.64583333333333
- tempo0: 144
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 18.51923076923077
- bar_density_p90: 25.4
- tracks: 2
- pitch_min: 25
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
- dynamic_windows: w00-w02:+7, w03-w11:+5, w12-w12:+9
- lead_notes: 281
- lead_from_melody_track: 272 (96.8%)
- lead_from_top_note: 281 (100.0%)
- fallback_lead_notes: 9
- support_notes_pruned: 90
- chromatic_tokens: 411
