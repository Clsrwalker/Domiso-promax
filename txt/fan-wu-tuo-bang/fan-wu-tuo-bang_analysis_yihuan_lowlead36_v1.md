# Analysis (Yihuan 36-Key LowLead36 Script): fan-wu-tuo-bang.mid

## Metrics
- note_count: 1140
- duration_s: 148.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.405405405405405
- bar_density_p90: 21.0
- tracks: 2
- pitch_min: 43
- pitch_max: 79

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
- octave_windows: w00-w18:+0
- lead_notes: 640
- lead_from_melody_track: 639 (99.8%)
- lead_from_top_note: 640 (100.0%)
- fallback_lead_notes: 1
- lead_lowlead_moved: 279
- lead_lowrow_notes: 416
- lead_midrow_notes: 53
- lead_highrow_notes: 0
- lead_ornaments_dropped: 11
- support_notes_pruned: 357
- chromatic_tokens: 34
