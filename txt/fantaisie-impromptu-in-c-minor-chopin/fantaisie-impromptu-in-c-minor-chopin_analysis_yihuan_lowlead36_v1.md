# Analysis (Yihuan 36-Key LowLead36 Script): fantaisie-impromptu-in-c-minor-chopin.mid

## Metrics
- note_count: 3049
- duration_s: 327.51022460328124
- tempo0: 168
- tempo_events: 38
- time_sig: 2/2
- max_poly: 6
- bar_density_mean: 22.094202898550726
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
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
- lead_notes: 1651
- lead_from_melody_track: 1605 (97.2%)
- lead_from_top_note: 1651 (100.0%)
- fallback_lead_notes: 46
- lead_lowlead_moved: 1405
- lead_lowrow_notes: 1447
- lead_midrow_notes: 150
- lead_highrow_notes: 0
- lead_ornaments_dropped: 251
- support_notes_pruned: 1159
- chromatic_tokens: 876
