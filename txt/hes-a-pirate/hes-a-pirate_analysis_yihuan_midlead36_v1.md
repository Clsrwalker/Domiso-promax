# Analysis (Yihuan 36-Key MidLead36 Script): hes-a-pirate.mid

## Metrics
- note_count: 1285
- duration_s: 78.52857504814025
- tempo0: 207
- tempo_events: 7
- time_sig: 6/8
- max_poly: 6
- bar_density_mean: 14.94186046511628
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 26
- pitch_max: 84

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
- base_shift: 12
- octave_windows: w00-w15:+12
- lead_notes: 328
- lead_from_melody_track: 273 (83.2%)
- lead_from_top_note: 328 (100.0%)
- fallback_lead_notes: 55
- lead_midlead_moved: 194
- lead_midrow_notes: 217
- lead_highrow_notes: 6
- support_notes_pruned: 2
- chromatic_tokens: 85
