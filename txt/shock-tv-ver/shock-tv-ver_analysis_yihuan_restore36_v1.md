# Analysis (Yihuan 36-Key Restore36 Script): shock-tv-ver.mid

## Metrics
- note_count: 329
- duration_s: 83.48007246376811
- tempo0: 69
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.708333333333334
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 40
- pitch_max: 85

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
- octave_windows: w00-w05:+12
- lead_notes: 137
- lead_from_melody_track: 134 (97.8%)
- lead_from_top_note: 137 (100.0%)
- fallback_lead_notes: 3
- support_notes_pruned: 2
- chromatic_tokens: 236
