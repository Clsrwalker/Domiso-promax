# Analysis (Yihuan 36-Key MidLead36 Script): rondo-alla-turca-turkish-march.mid

## Metrics
- note_count: 2944
- duration_s: 233.04545454545453
- tempo0: 120
- tempo_events: 3
- time_sig: 2/8
- max_poly: 8
- bar_density_mean: 6.331182795698925
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 34
- pitch_max: 88

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
- lead_notes: 1180
- lead_from_melody_track: 1176 (99.7%)
- lead_from_top_note: 1180 (100.0%)
- fallback_lead_notes: 4
- lead_midlead_moved: 901
- lead_midrow_notes: 1046
- lead_highrow_notes: 67
- support_notes_pruned: 131
- chromatic_tokens: 667
