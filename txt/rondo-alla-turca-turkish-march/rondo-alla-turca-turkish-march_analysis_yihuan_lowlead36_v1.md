# Analysis (Yihuan 36-Key LowLead36 Script): rondo-alla-turca-turkish-march.mid

## Metrics
- note_count: 2944
- duration_s: 233.04545454545453
- tempo0: 120
- tempo_events: 3
- time_sig: 2/8
- max_poly: 8
- bar_density_mean: 6.331182795698925
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 34
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
- base_shift: 0
- octave_windows: w00-w29:+0
- lead_notes: 1180
- lead_from_melody_track: 1176 (99.7%)
- lead_from_top_note: 1072 (90.8%)
- fallback_lead_notes: 4
- lead_lowlead_moved: 1094
- lead_lowrow_notes: 1016
- lead_midrow_notes: 82
- lead_highrow_notes: 0
- lead_ornaments_dropped: 322
- support_notes_pruned: 1272
- chromatic_tokens: 249
