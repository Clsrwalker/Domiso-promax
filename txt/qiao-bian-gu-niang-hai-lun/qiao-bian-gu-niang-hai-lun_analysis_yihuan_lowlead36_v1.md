# Analysis (Yihuan 36-Key LowLead36 Script): qiao-bian-gu-niang-hai-lun.mid

## Metrics
- note_count: 836
- duration_s: 182.33766233766235
- tempo0: 77
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 14.413793103448276
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 39
- pitch_max: 84

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
- lead_notes: 371
- lead_from_melody_track: 366 (98.7%)
- lead_from_top_note: 348 (93.8%)
- fallback_lead_notes: 5
- lead_lowlead_moved: 305
- lead_lowrow_notes: 287
- lead_midrow_notes: 22
- lead_highrow_notes: 0
- lead_ornaments_dropped: 15
- support_notes_pruned: 290
- chromatic_tokens: 270
