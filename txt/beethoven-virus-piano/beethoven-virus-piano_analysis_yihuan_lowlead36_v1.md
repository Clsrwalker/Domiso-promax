# Analysis (Yihuan 36-Key LowLead36 Script): beethoven-virus-piano.mid

## Metrics
- note_count: 2671
- duration_s: 216.73125
- tempo0: 160
- tempo_events: 3
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.07857142857143
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 21
- pitch_max: 100

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
- octave_windows: w00-w34:+0
- lead_notes: 1069
- lead_from_melody_track: 1012 (94.7%)
- lead_from_top_note: 1014 (94.9%)
- fallback_lead_notes: 57
- lead_lowlead_moved: 887
- lead_lowrow_notes: 887
- lead_midrow_notes: 98
- lead_highrow_notes: 0
- lead_ornaments_dropped: 108
- support_notes_pruned: 1043
- chromatic_tokens: 156
