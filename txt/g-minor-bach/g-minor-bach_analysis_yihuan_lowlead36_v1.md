# Analysis (Yihuan 36-Key LowLead36 Script): g-minor-bach.mid

## Metrics
- note_count: 1810
- duration_s: 158.28
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 27.424242424242426
- bar_density_p90: 34.0
- tracks: 3
- pitch_min: 34
- pitch_max: 80

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
- lead_notes: 258
- lead_from_melody_track: 8 (3.1%)
- lead_from_top_note: 238 (92.2%)
- fallback_lead_notes: 250
- lead_lowlead_moved: 197
- lead_lowrow_notes: 232
- lead_midrow_notes: 19
- lead_highrow_notes: 0
- lead_ornaments_dropped: 4
- support_notes_pruned: 1327
- chromatic_tokens: 124
