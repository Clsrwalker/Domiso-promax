# Analysis (Yihuan 36-Key MidLead36 Script): yan-yuan-xue-zhi-qian.mid

## Metrics
- note_count: 896
- duration_s: 132.2400442477876
- tempo0: 120
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.575757575757576
- bar_density_p90: 20.3
- tracks: 2
- pitch_min: 16
- pitch_max: 102

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
- octave_windows: w00-w16:+0
- lead_notes: 390
- lead_from_melody_track: 377 (96.7%)
- lead_from_top_note: 390 (100.0%)
- fallback_lead_notes: 13
- lead_midlead_moved: 221
- lead_midrow_notes: 293
- lead_highrow_notes: 15
- support_notes_pruned: 93
- chromatic_tokens: 575
