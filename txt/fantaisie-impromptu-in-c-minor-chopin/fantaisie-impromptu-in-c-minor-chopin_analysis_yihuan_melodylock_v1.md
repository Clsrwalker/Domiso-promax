# Analysis (Yihuan 36-Key MelodyLock Script): fantaisie-impromptu-in-c-minor-chopin.mid

## Metrics
- note_count: 3049
- duration_s: 327.51022460328124
- tempo0: 168
- tempo_events: 38
- time_sig: 2/2
- max_poly: 6
- bar_density_mean: 22.094202898550726
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 100

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
- dynamic_windows: w00-w23:+2, w24-w28:-1, w29-w34:+5
- lead_notes: 1663
- lead_from_melody_track: 1605 (96.5%)
- lead_from_top_note: 1663 (100.0%)
- fallback_lead_notes: 58
- support_notes_pruned: 325
- chromatic_tokens: 1563
