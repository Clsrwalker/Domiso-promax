# Analysis (Yihuan 36-Key LowLead36 Script): sis-puella-magica-puella-magi-madoka-magica-yuki-kajiura.mid

## Metrics
- note_count: 1386
- duration_s: 189.5
- tempo0: 120
- tempo_events: 1
- time_sig: 3/4
- max_poly: 9
- bar_density_mean: 11.0
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 27
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
- octave_windows: w00-w23:+0
- lead_notes: 406
- lead_from_melody_track: 392 (96.6%)
- lead_from_top_note: 372 (91.6%)
- fallback_lead_notes: 14
- lead_lowlead_moved: 327
- lead_lowrow_notes: 312
- lead_midrow_notes: 52
- lead_highrow_notes: 0
- lead_ornaments_dropped: 0
- support_notes_pruned: 539
- chromatic_tokens: 165
