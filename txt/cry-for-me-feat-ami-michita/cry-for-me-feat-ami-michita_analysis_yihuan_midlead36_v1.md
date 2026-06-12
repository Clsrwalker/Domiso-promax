# Analysis (Yihuan 36-Key MidLead36 Script): cry-for-me-feat-ami-michita.mid

## Metrics
- note_count: 1508
- duration_s: 239.9673913043478
- tempo0: 92
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 16.391304347826086
- bar_density_p90: 22.7
- tracks: 2
- pitch_min: 38
- pitch_max: 94

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
- octave_windows: w00-w22:+0
- lead_notes: 665
- lead_from_melody_track: 658 (98.9%)
- lead_from_top_note: 665 (100.0%)
- fallback_lead_notes: 7
- lead_midlead_moved: 399
- lead_midrow_notes: 456
- lead_highrow_notes: 39
- support_notes_pruned: 4
- chromatic_tokens: 380
