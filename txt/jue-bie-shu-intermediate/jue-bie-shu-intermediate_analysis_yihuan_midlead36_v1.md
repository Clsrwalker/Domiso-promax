# Analysis (Yihuan 36-Key MidLead36 Script): jue-bie-shu-intermediate.mid

## Metrics
- note_count: 1607
- duration_s: 249.2121212121212
- tempo0: 90
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 14.87962962962963
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 26
- pitch_max: 98

## Recommended Profile
- yihuan_midlead36_dense
- reason: dense piano texture -> yihuan_midlead36_dense

## Yihuan 36-Key MidLead36 Intent
- preserve literal rhythm/body more aggressively than melodylock
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A as the lead anchor and prefer the middle row C4-B4
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- retain more source harmony in B/C than melodylock
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 0
- octave_windows: w00-w26:+0
- lead_notes: 571
- lead_from_melody_track: 570 (99.8%)
- lead_from_top_note: 571 (100.0%)
- fallback_lead_notes: 1
- lead_midlead_moved: 397
- lead_midrow_notes: 515
- lead_highrow_notes: 4
- support_notes_pruned: 13
- chromatic_tokens: 171
