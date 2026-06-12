# Analysis (Yihuan 36-Key MelodyLock Script): wamozart-symphony-no40-in-gm-k550-1st-mvt.mid

## Metrics
- note_count: 5533
- duration_s: 455.4
- tempo0: 210
- tempo_events: 1
- time_sig: 2/2
- max_poly: 7
- bar_density_mean: 13.867167919799499
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 36
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
- base_shift: -1
- dynamic_windows: w00-w14:+1, w15-w24:-3, w25-w99:-1
- lead_notes: 2294
- lead_from_melody_track: 2015 (87.8%)
- lead_from_top_note: 2222 (96.9%)
- fallback_lead_notes: 279
- support_notes_pruned: 10
- chromatic_tokens: 2365
