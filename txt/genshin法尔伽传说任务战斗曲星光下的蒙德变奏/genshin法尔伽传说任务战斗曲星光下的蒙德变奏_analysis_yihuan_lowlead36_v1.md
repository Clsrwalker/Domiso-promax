# Analysis (Yihuan 36-Key LowLead36 Script): genshin法尔伽传说任务战斗曲星光下的蒙德变奏.mid

## Metrics
- note_count: 946
- duration_s: 162.7215189873418
- tempo0: 158
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 8.841121495327103
- bar_density_p90: 12.2
- tracks: 2
- pitch_min: 33
- pitch_max: 81

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
- octave_windows: w00-w26:+12
- lead_notes: 397
- lead_from_melody_track: 372 (93.7%)
- lead_from_top_note: 387 (97.5%)
- fallback_lead_notes: 25
- lead_lowlead_moved: 338
- lead_lowrow_notes: 335
- lead_midrow_notes: 14
- lead_highrow_notes: 0
- lead_ornaments_dropped: 9
- support_notes_pruned: 402
- chromatic_tokens: 70
