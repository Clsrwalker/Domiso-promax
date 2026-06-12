# Analysis (Yihuan 36-Key LowLead36 Script): ai-he-jiang-xue-er.mid

## Metrics
- note_count: 1017
- duration_s: 220.0
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.646153846153846
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 39
- pitch_max: 83

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
- octave_windows: w00-w16:+0
- lead_notes: 483
- lead_from_melody_track: 476 (98.6%)
- lead_from_top_note: 483 (100.0%)
- fallback_lead_notes: 7
- lead_lowlead_moved: 350
- lead_lowrow_notes: 308
- lead_midrow_notes: 76
- lead_highrow_notes: 0
- lead_ornaments_dropped: 26
- support_notes_pruned: 376
- chromatic_tokens: 317
