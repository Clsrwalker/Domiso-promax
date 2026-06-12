# Analysis (Yihuan 36-Key MidLead36 Script): poesy-of-chrysolite.mid

## Metrics
- note_count: 1163
- duration_s: 139.41195568280182
- tempo0: 94
- tempo_events: 11
- time_sig: 1/8
- max_poly: 7
- bar_density_mean: 2.60762331838565
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 31
- pitch_max: 91

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
- octave_windows: w00-w13:+0
- lead_notes: 326
- lead_from_melody_track: 274 (84.0%)
- lead_from_top_note: 326 (100.0%)
- fallback_lead_notes: 52
- lead_midlead_moved: 186
- lead_midrow_notes: 254
- lead_highrow_notes: 27
- support_notes_pruned: 92
- chromatic_tokens: 341
