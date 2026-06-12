# Analysis (Yihuan 36-Key LowLead36 Script): moonlight-sonata-3rd-movement.mid

## Metrics
- note_count: 6414
- duration_s: 374.8058823529412
- tempo0: 170
- tempo_events: 3
- time_sig: 4/4
- max_poly: 10
- bar_density_mean: 24.295454545454547
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 29
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
- octave_windows: w00-w65:+0
- lead_notes: 2385
- lead_from_melody_track: 2283 (95.7%)
- lead_from_top_note: 2233 (93.6%)
- fallback_lead_notes: 102
- lead_lowlead_moved: 1827
- lead_lowrow_notes: 1807
- lead_midrow_notes: 309
- lead_highrow_notes: 0
- lead_ornaments_dropped: 270
- support_notes_pruned: 2909
- chromatic_tokens: 1443
