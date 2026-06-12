# Analysis (Yihuan 36-Key MidLead36 Script): rolling-in-the-deep-adele.mid

## Metrics
- note_count: 1007
- duration_s: 127.09499999999998
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.0
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 43
- pitch_max: 86

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
- lead_notes: 321
- lead_from_melody_track: 298 (92.8%)
- lead_from_top_note: 319 (99.4%)
- fallback_lead_notes: 23
- lead_midlead_moved: 90
- lead_midrow_notes: 222
- lead_highrow_notes: 0
- support_notes_pruned: 78
- chromatic_tokens: 262
