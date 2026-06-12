# Analysis (Yihuan 36-Key MidLead36 Script): 虚空鼓动，劫火高扬.mid

## Metrics
- note_count: 1441
- duration_s: 193.97362442756955
- tempo0: 82
- tempo_events: 14
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 17.36144578313253
- bar_density_p90: 25.6
- tracks: 2
- pitch_min: 36
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
- octave_windows: w00-w20:+0
- lead_notes: 543
- lead_from_melody_track: 525 (96.7%)
- lead_from_top_note: 542 (99.8%)
- fallback_lead_notes: 18
- lead_midlead_moved: 274
- lead_midrow_notes: 420
- lead_highrow_notes: 29
- support_notes_pruned: 2
- chromatic_tokens: 239
