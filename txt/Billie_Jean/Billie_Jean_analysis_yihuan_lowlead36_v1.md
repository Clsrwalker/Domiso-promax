# Analysis (Yihuan 36-Key LowLead36 Script): Billie_Jean.mid

## Metrics
- note_count: 5972
- duration_s: 294.91525423728814
- tempo0: 118
- tempo_events: 1
- time_sig: 4/4
- max_poly: 13
- bar_density_mean: 41.186206896551724
- bar_density_p90: 50.0
- tracks: 9
- pitch_min: 30
- pitch_max: 85

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
- octave_windows: w00-w36:+12
- lead_notes: 1156
- lead_from_melody_track: 1140 (98.6%)
- lead_from_top_note: 1152 (99.7%)
- fallback_lead_notes: 16
- lead_lowlead_moved: 3
- lead_lowrow_notes: 4
- lead_midrow_notes: 0
- lead_highrow_notes: 0
- lead_ornaments_dropped: 1
- support_notes_pruned: 3133
- chromatic_tokens: 453
