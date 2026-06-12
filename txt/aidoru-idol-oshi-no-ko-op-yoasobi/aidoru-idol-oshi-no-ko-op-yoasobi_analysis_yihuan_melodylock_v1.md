# Analysis (Yihuan 36-Key MelodyLock Script): aidoru-idol-oshi-no-ko-op-yoasobi.mid

## Metrics
- note_count: 1018
- duration_s: 79.14110429447852
- tempo0: 163
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 18.85185185185185
- bar_density_p90: 25.0
- tracks: 2
- pitch_min: 27
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
- base_shift: 2
- dynamic_windows: w00-w01:+1, w02-w08:+5, w09-w13:-1
- lead_notes: 333
- lead_from_melody_track: 332 (99.7%)
- lead_from_top_note: 333 (100.0%)
- fallback_lead_notes: 1
- support_notes_pruned: 35
- chromatic_tokens: 447
