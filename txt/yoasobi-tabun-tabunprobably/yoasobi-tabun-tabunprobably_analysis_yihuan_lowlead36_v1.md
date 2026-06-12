# Analysis (Yihuan 36-Key LowLead36 Script): yoasobi-tabun-tabunprobably.mid

## Metrics
- note_count: 1836
- duration_s: 257.5
- tempo0: 90
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 18.927835051546392
- bar_density_p90: 26.2
- tracks: 2
- pitch_min: 42
- pitch_max: 94

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
- base_shift: 0
- octave_windows: w00-w24:+0
- lead_notes: 661
- lead_from_melody_track: 620 (93.8%)
- lead_from_top_note: 657 (99.4%)
- fallback_lead_notes: 41
- lead_lowlead_moved: 527
- lead_lowrow_notes: 482
- lead_midrow_notes: 81
- lead_highrow_notes: 0
- lead_ornaments_dropped: 18
- support_notes_pruned: 811
- chromatic_tokens: 253
