# Analysis (Yihuan 36-Key LowLead36 Script): to-the-end-of-all-wars.mid

## Metrics
- note_count: 2910
- duration_s: 208.66071428571428
- tempo0: 112
- tempo_events: 1
- time_sig: 1/4
- max_poly: 12
- bar_density_mean: 7.461538461538462
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 21
- pitch_max: 95

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
- lead_notes: 890
- lead_from_melody_track: 871 (97.9%)
- lead_from_top_note: 711 (79.9%)
- fallback_lead_notes: 19
- lead_lowlead_moved: 642
- lead_lowrow_notes: 653
- lead_midrow_notes: 117
- lead_highrow_notes: 0
- lead_ornaments_dropped: 25
- support_notes_pruned: 1004
- chromatic_tokens: 522
