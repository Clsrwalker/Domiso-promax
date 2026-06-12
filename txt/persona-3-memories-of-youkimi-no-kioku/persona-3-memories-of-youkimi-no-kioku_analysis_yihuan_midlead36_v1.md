# Analysis (Yihuan 36-Key MidLead36 Script): persona-3-memories-of-youkimi-no-kioku.mid

## Metrics
- note_count: 1033
- duration_s: 137.58165113871635
- tempo0: 115
- tempo_events: 5
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 16.140625
- bar_density_p90: 21.0
- tracks: 2
- pitch_min: 31
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
- octave_windows: w00-w15:+0
- lead_notes: 396
- lead_from_melody_track: 374 (94.4%)
- lead_from_top_note: 393 (99.2%)
- fallback_lead_notes: 22
- lead_midlead_moved: 206
- lead_midrow_notes: 242
- lead_highrow_notes: 10
- support_notes_pruned: 98
- chromatic_tokens: 234
