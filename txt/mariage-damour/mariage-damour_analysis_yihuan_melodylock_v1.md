# Analysis (Yihuan 36-Key MelodyLock Script): mariage-damour.mid

## Metrics
- note_count: 1631
- duration_s: 226.62895927601807
- tempo0: 90
- tempo_events: 4
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.188235294117646
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 26
- pitch_max: 110

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
- base_shift: -7
- dynamic_windows: w00-w09:-6, w10-w11:-10, w12-w21:-8
- lead_notes: 925
- lead_from_melody_track: 859 (92.9%)
- lead_from_top_note: 925 (100.0%)
- fallback_lead_notes: 66
- support_notes_pruned: 267
- chromatic_tokens: 578
