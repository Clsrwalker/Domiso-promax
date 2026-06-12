# Analysis (Yihuan 36-Key LowLead36 Script): the-raising-fighting-spirit.mid

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
- yihuan_lowlead36_dense
- reason: dense piano texture -> yihuan_lowlead36_dense

## Yihuan 36-Key LowLead36 Intent
- prioritize a recognizable low-register lead over piano figurations
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A mostly in the low row C3-B3 (Z X C V B N M) and smooth out tiny ornament notes
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- simplify accompaniment into sparse upper support and occasional bass anchors
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 12
- octave_windows: w00-w12:+12
- lead_notes: 339
- lead_from_melody_track: 338 (99.7%)
- lead_from_top_note: 313 (92.3%)
- fallback_lead_notes: 1
- lead_lowlead_moved: 243
- lead_lowrow_notes: 237
- lead_midrow_notes: 7
- lead_highrow_notes: 0
- lead_ornaments_dropped: 25
- support_notes_pruned: 445
- chromatic_tokens: 42
