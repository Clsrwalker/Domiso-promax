# Analysis (Yihuan 36-Key Restore36 Script): beat-it.mid

## Metrics
- note_count: 1282
- duration_s: 116.0
- tempo0: 135
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.424242424242426
- bar_density_p90: 22.0
- tracks: 4
- pitch_min: 36
- pitch_max: 84

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
- octave_windows: w00-w16:+12
- lead_notes: 391
- lead_from_melody_track: 239 (61.1%)
- lead_from_top_note: 391 (100.0%)
- fallback_lead_notes: 152
- support_notes_pruned: 2
- chromatic_tokens: 267
