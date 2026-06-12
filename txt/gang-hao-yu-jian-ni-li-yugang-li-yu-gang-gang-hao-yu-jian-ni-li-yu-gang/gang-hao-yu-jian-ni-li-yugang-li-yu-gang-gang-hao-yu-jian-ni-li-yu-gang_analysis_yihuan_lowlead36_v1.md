# Analysis (Yihuan 36-Key LowLead36 Script): gang-hao-yu-jian-ni-li-yugang-li-yu-gang-gang-hao-yu-jian-ni-li-yu-gang.mid

## Metrics
- note_count: 1130
- duration_s: 190.1314935064935
- tempo0: 77
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 18.524590163934427
- bar_density_p90: 26.8
- tracks: 2
- pitch_min: 23
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
- octave_windows: w00-w15:+0
- lead_notes: 370
- lead_from_melody_track: 356 (96.2%)
- lead_from_top_note: 341 (92.2%)
- fallback_lead_notes: 14
- lead_lowlead_moved: 238
- lead_lowrow_notes: 204
- lead_midrow_notes: 80
- lead_highrow_notes: 0
- lead_ornaments_dropped: 12
- support_notes_pruned: 394
- chromatic_tokens: 365
