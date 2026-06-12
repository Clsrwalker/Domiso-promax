# Analysis (Yihuan 36-Key LowLead36 Script): ballade-pour-adeline-richard-clayderman.mid

## Metrics
- note_count: 912
- duration_s: 174.7543530772633
- tempo0: 60
- tempo_events: 11
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 21.209302325581394
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 93

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
- base_shift: -12
- octave_windows: w00-w10:-12
- lead_notes: 390
- lead_from_melody_track: 352 (90.3%)
- lead_from_top_note: 346 (88.7%)
- fallback_lead_notes: 38
- lead_lowlead_moved: 142
- lead_lowrow_notes: 248
- lead_midrow_notes: 25
- lead_highrow_notes: 0
- lead_ornaments_dropped: 40
- support_notes_pruned: 286
- chromatic_tokens: 6
