# Analysis (Yihuan 36-Key LowLead36 Script): mystery-of-love.mid

## Metrics
- note_count: 1571
- duration_s: 201.85
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.71
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 47
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
- octave_windows: w00-w24:+0
- lead_notes: 419
- lead_from_melody_track: 410 (97.9%)
- lead_from_top_note: 378 (90.2%)
- fallback_lead_notes: 9
- lead_lowlead_moved: 376
- lead_lowrow_notes: 379
- lead_midrow_notes: 6
- lead_highrow_notes: 0
- lead_ornaments_dropped: 17
- support_notes_pruned: 841
- chromatic_tokens: 48
