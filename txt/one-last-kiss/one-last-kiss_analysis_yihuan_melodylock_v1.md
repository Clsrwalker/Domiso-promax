# Analysis (Yihuan 36-Key MelodyLock Script): one-last-kiss.mid

## Metrics
- note_count: 2095
- duration_s: 246.9494494047619
- tempo0: 112
- tempo_events: 4
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 18.37719298245614
- bar_density_p90: 27.0
- tracks: 2
- pitch_min: 37
- pitch_max: 99

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
- base_shift: 3
- dynamic_windows: w00-w18:+3, w19-w22:+6, w23-w28:+0
- lead_notes: 790
- lead_from_melody_track: 776 (98.2%)
- lead_from_top_note: 790 (100.0%)
- fallback_lead_notes: 14
- support_notes_pruned: 83
- chromatic_tokens: 539
