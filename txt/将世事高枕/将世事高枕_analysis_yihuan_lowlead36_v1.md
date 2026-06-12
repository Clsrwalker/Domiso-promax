# Analysis (Yihuan 36-Key LowLead36 Script): 将世事高枕.mid

## Metrics
- note_count: 679
- duration_s: 133.84855769230768
- tempo0: 104
- tempo_events: 2
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 11.912280701754385
- bar_density_p90: 17.4
- tracks: 2
- pitch_min: 37
- pitch_max: 87

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
- octave_windows: w00-w14:+0
- lead_notes: 275
- lead_from_melody_track: 258 (93.8%)
- lead_from_top_note: 274 (99.6%)
- fallback_lead_notes: 17
- lead_lowlead_moved: 219
- lead_lowrow_notes: 197
- lead_midrow_notes: 53
- lead_highrow_notes: 0
- lead_ornaments_dropped: 4
- support_notes_pruned: 332
- chromatic_tokens: 225
