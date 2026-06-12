# Analysis (Yihuan 36-Key LowLead36 Script): wamozart-symphony-no40-in-gm-k550-1st-mvt.mid

## Metrics
- note_count: 5533
- duration_s: 455.4
- tempo0: 210
- tempo_events: 1
- time_sig: 2/2
- max_poly: 7
- bar_density_mean: 13.867167919799499
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 36
- pitch_max: 91

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
- octave_windows: w00-w99:+0
- lead_notes: 2129
- lead_from_melody_track: 2015 (94.6%)
- lead_from_top_note: 1892 (88.9%)
- fallback_lead_notes: 114
- lead_lowlead_moved: 1684
- lead_lowrow_notes: 1626
- lead_midrow_notes: 220
- lead_highrow_notes: 0
- lead_ornaments_dropped: 60
- support_notes_pruned: 2064
- chromatic_tokens: 936
