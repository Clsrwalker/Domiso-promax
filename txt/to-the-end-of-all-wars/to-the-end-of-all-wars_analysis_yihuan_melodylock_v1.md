# Analysis (Yihuan 36-Key MelodyLock Script): to-the-end-of-all-wars.mid

## Metrics
- note_count: 2910
- duration_s: 208.66071428571428
- tempo0: 112
- tempo_events: 1
- time_sig: 1/4
- max_poly: 12
- bar_density_mean: 7.461538461538462
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 21
- pitch_max: 95

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
- base_shift: 5
- dynamic_windows: w00-w10:+8, w11-w18:+2, w19-w24:+5
- lead_notes: 896
- lead_from_melody_track: 871 (97.2%)
- lead_from_top_note: 893 (99.7%)
- fallback_lead_notes: 25
- support_notes_pruned: 117
- chromatic_tokens: 1282
