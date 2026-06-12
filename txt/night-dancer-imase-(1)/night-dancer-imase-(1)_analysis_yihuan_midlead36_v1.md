# Analysis (Yihuan 36-Key MidLead36 Script): night-dancer-imase (1).mid

## Metrics
- note_count: 2526
- duration_s: 208.47669491525423
- tempo0: 118
- tempo_events: 2
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 25.00990099009901
- bar_density_p90: 34.0
- tracks: 2
- pitch_min: 24
- pitch_max: 98

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
- octave_windows: w00-w25:+0
- lead_notes: 617
- lead_from_melody_track: 610 (98.9%)
- lead_from_top_note: 616 (99.8%)
- fallback_lead_notes: 7
- lead_midlead_moved: 531
- lead_midrow_notes: 533
- lead_highrow_notes: 0
- support_notes_pruned: 181
- chromatic_tokens: 787
