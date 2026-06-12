# Analysis (Yihuan 36-Key LowLead36 Script): 銀色飛行船.mid

## Metrics
- note_count: 932
- duration_s: 227.41544117647058
- tempo0: 68
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 14.338461538461539
- bar_density_p90: 23.4
- tracks: 5
- pitch_min: 37
- pitch_max: 77

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
- octave_windows: w00-w16:+12
- lead_notes: 358
- lead_from_melody_track: 309 (86.3%)
- lead_from_top_note: 337 (94.1%)
- fallback_lead_notes: 49
- lead_lowlead_moved: 269
- lead_lowrow_notes: 233
- lead_midrow_notes: 43
- lead_highrow_notes: 0
- lead_ornaments_dropped: 32
- support_notes_pruned: 179
- chromatic_tokens: 266
