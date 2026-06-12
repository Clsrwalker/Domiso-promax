# Analysis (Yihuan 36-Key Ballad36 Script): genshin法尔伽传说任务战斗曲星光下的蒙德变奏.mid

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
- yihuan_ballad36_dense
- reason: dense piano texture -> yihuan_ballad36_dense

## Yihuan 36-Key Ballad36 Intent
- prioritize a singable vocal-like lead over piano figurations
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A in the middle row whenever possible and smooth out tiny ornament notes
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- simplify accompaniment into soft harmonic pads and bass anchors
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 12
- octave_windows: w00-w26:+12
- lead_notes: 399
- lead_from_melody_track: 372 (93.2%)
- lead_from_top_note: 366 (91.7%)
- fallback_lead_notes: 27
- lead_midlead_moved: 282
- lead_midrow_notes: 334
- lead_highrow_notes: 13
- lead_ornaments_dropped: 9
- support_notes_pruned: 38
- chromatic_tokens: 85
