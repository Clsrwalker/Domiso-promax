# Analysis (Yihuan 36-Key Restore36 Script): golden-hour.mid

## Metrics
- note_count: 1073
- duration_s: 90.0
- tempo0: 96
- tempo_events: 1
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 44.708333333333336
- bar_density_p90: 59.0
- tracks: 2
- pitch_min: 40
- pitch_max: 92

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
- base_shift: 0
- octave_windows: w00-w08:+0
- lead_notes: 447
- lead_from_melody_track: 447 (100.0%)
- lead_from_top_note: 447 (100.0%)
- fallback_lead_notes: 0
- support_notes_pruned: 5
- chromatic_tokens: 611
