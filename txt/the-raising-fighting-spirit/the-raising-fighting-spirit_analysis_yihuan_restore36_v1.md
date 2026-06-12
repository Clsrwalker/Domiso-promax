# Analysis (Yihuan 36-Key Restore36 Script): the-raising-fighting-spirit.mid

## Metrics
- note_count: 1083
- duration_s: 85.62857142857143
- tempo0: 140
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 21.66
- bar_density_p90: 35.6
- tracks: 2
- pitch_min: 28
- pitch_max: 88

## Recommended Profile
- yihuan_restore36_dense
- reason: dense piano texture -> yihuan_restore36_dense

## Yihuan 36-Key Restore36 Intent
- preserve literal rhythm/body more aggressively than melodylock
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A as the lead anchor but retain more source harmony in B/C
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 12
- octave_windows: w00-w12:+12
- lead_notes: 339
- lead_from_melody_track: 338 (99.7%)
- lead_from_top_note: 339 (100.0%)
- fallback_lead_notes: 1
- support_notes_pruned: 61
- chromatic_tokens: 100
