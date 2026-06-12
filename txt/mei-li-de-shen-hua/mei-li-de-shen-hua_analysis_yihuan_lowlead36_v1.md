# Analysis (Yihuan 36-Key LowLead36 Script): mei-li-de-shen-hua.mid

## Metrics
- note_count: 1820
- duration_s: 314.0
- tempo0: 60
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 23.636363636363637
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 29
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
- octave_windows: w00-w19:+0
- lead_notes: 470
- lead_from_melody_track: 462 (98.3%)
- lead_from_top_note: 393 (83.6%)
- fallback_lead_notes: 8
- lead_lowlead_moved: 393
- lead_lowrow_notes: 321
- lead_midrow_notes: 94
- lead_highrow_notes: 0
- lead_ornaments_dropped: 36
- support_notes_pruned: 859
- chromatic_tokens: 160
