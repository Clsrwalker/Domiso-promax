# Analysis (Yihuan 36-Key Restore36 Script): luv-letter.mid

## Metrics
- note_count: 1921
- duration_s: 295.4516979600596
- tempo0: 80
- tempo_events: 15
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.404040404040405
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 34
- pitch_max: 101

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
- base_shift: -12
- octave_windows: w00-w24:-12
- lead_notes: 927
- lead_from_melody_track: 907 (97.8%)
- lead_from_top_note: 924 (99.7%)
- fallback_lead_notes: 20
- support_notes_pruned: 41
- chromatic_tokens: 1186
