# Analysis (Yihuan 36-Key MidLead36 Script): etude-s-1413-in-g-minor-la-campanella-liszt.mid

## Metrics
- note_count: 4123
- duration_s: 292.35995179818656
- tempo0: 102
- tempo_events: 26
- time_sig: 6/8
- max_poly: 8
- bar_density_mean: 28.832167832167833
- bar_density_p90: 45.6
- tracks: 2
- pitch_min: 27
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
- base_shift: -12
- octave_windows: w00-w26:-12
- lead_notes: 1531
- lead_from_melody_track: 1500 (98.0%)
- lead_from_top_note: 1527 (99.7%)
- fallback_lead_notes: 31
- lead_midlead_moved: 760
- lead_midrow_notes: 1140
- lead_highrow_notes: 19
- support_notes_pruned: 231
- chromatic_tokens: 1817
