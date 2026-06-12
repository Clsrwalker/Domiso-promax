# Analysis (Yihuan 36-Key LowLead36 Script): kiss-the-rain-yiruma.mid

## Metrics
- note_count: 1052
- duration_s: 266.49997201074785
- tempo0: 63
- tempo_events: 8
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.701492537313433
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 33
- pitch_max: 97

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
- lead_notes: 394
- lead_from_melody_track: 392 (99.5%)
- lead_from_top_note: 379 (96.2%)
- fallback_lead_notes: 2
- lead_lowlead_moved: 296
- lead_lowrow_notes: 276
- lead_midrow_notes: 26
- lead_highrow_notes: 0
- lead_ornaments_dropped: 26
- support_notes_pruned: 412
- chromatic_tokens: 257
