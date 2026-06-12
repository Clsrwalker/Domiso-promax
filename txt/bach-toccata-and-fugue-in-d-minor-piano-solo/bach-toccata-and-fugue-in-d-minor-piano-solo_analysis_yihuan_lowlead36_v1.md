# Analysis (Yihuan 36-Key LowLead36 Script): bach-toccata-and-fugue-in-d-minor-piano-solo.mid

## Metrics
- note_count: 4122
- duration_s: 439.1054577532607
- tempo0: 60
- tempo_events: 46
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 28.825174825174827
- bar_density_p90: 48.0
- tracks: 2
- pitch_min: 20
- pitch_max: 86

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
- octave_windows: w00-w35:+0
- lead_notes: 1619
- lead_from_melody_track: 1522 (94.0%)
- lead_from_top_note: 1539 (95.1%)
- fallback_lead_notes: 97
- lead_lowlead_moved: 1263
- lead_lowrow_notes: 1316
- lead_midrow_notes: 191
- lead_highrow_notes: 0
- lead_ornaments_dropped: 304
- support_notes_pruned: 1684
- chromatic_tokens: 309
