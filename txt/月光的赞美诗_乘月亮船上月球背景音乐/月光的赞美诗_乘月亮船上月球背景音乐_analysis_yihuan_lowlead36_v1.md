# Analysis (Yihuan 36-Key LowLead36 Script): 月光的赞美诗_乘月亮船上月球背景音乐.mid

## Metrics
- note_count: 1054
- duration_s: 193.29427083333334
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 11.094736842105263
- bar_density_p90: 17.0
- tracks: 2
- pitch_min: 34
- pitch_max: 101

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
- octave_windows: w00-w23:+0
- lead_notes: 418
- lead_from_melody_track: 399 (95.5%)
- lead_from_top_note: 416 (99.5%)
- fallback_lead_notes: 19
- lead_lowlead_moved: 368
- lead_lowrow_notes: 333
- lead_midrow_notes: 56
- lead_highrow_notes: 0
- lead_ornaments_dropped: 67
- support_notes_pruned: 393
- chromatic_tokens: 210
