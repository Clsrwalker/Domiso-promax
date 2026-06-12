# Analysis (Yihuan 36-Key LowLead36 Script): jue-bie-shu-intermediate.mid

## Metrics
- note_count: 1607
- duration_s: 249.2121212121212
- tempo0: 90
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 14.87962962962963
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 26
- pitch_max: 98

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
- octave_windows: w00-w26:+0
- lead_notes: 571
- lead_from_melody_track: 570 (99.8%)
- lead_from_top_note: 552 (96.7%)
- fallback_lead_notes: 1
- lead_lowlead_moved: 505
- lead_lowrow_notes: 495
- lead_midrow_notes: 12
- lead_highrow_notes: 0
- lead_ornaments_dropped: 80
- support_notes_pruned: 806
- chromatic_tokens: 26
