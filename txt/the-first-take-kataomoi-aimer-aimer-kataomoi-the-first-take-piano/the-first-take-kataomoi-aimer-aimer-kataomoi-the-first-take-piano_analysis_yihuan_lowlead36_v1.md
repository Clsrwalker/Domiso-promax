# Analysis (Yihuan 36-Key LowLead36 Script): the-first-take-kataomoi-aimer-aimer-kataomoi-the-first-take-piano.mid

## Metrics
- note_count: 1282
- duration_s: 205.36082474226805
- tempo0: 97
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 15.44578313253012
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 30
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
- octave_windows: w00-w20:+0
- lead_notes: 476
- lead_from_melody_track: 455 (95.6%)
- lead_from_top_note: 433 (91.0%)
- fallback_lead_notes: 21
- lead_lowlead_moved: 356
- lead_lowrow_notes: 346
- lead_midrow_notes: 87
- lead_highrow_notes: 0
- lead_ornaments_dropped: 38
- support_notes_pruned: 379
- chromatic_tokens: 466
