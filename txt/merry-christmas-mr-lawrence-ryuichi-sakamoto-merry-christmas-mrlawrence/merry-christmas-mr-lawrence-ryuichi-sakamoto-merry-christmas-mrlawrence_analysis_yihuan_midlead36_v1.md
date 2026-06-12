# Analysis (Yihuan 36-Key MidLead36 Script): merry-christmas-mr-lawrence-ryuichi-sakamoto-merry-christmas-mrlawrence.mid

## Metrics
- note_count: 3039
- duration_s: 289.4417582417582
- tempo0: 104
- tempo_events: 3
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 19.11320754716981
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 29
- pitch_max: 97

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
- octave_windows: w00-w29:+0
- lead_notes: 768
- lead_from_melody_track: 768 (100.0%)
- lead_from_top_note: 767 (99.9%)
- fallback_lead_notes: 0
- lead_midlead_moved: 448
- lead_midrow_notes: 577
- lead_highrow_notes: 21
- support_notes_pruned: 35
- chromatic_tokens: 1859
