# Analysis (Yihuan 36-Key Restore36 Script): nod-krai.mid

## Metrics
- note_count: 2539
- duration_s: 254.90157128257536
- tempo0: 76
- tempo_events: 2
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 24.650485436893202
- bar_density_p90: 38.0
- tracks: 2
- pitch_min: 21
- pitch_max: 99

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
- octave_windows: w00-w25:+0
- lead_notes: 713
- lead_from_melody_track: 707 (99.2%)
- lead_from_top_note: 695 (97.5%)
- fallback_lead_notes: 6
- support_notes_pruned: 73
- chromatic_tokens: 656
