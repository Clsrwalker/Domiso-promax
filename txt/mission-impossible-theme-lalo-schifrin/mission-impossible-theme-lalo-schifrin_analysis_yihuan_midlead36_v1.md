# Analysis (Yihuan 36-Key MidLead36 Script): mission-impossible-theme-lalo-schifrin.mid

## Metrics
- note_count: 2756
- duration_s: 193.805
- tempo0: 100
- tempo_events: 3
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 25.51851851851852
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 26
- pitch_max: 108

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
- lead_notes: 838
- lead_from_melody_track: 824 (98.3%)
- lead_from_top_note: 791 (94.4%)
- fallback_lead_notes: 14
- lead_midlead_moved: 419
- lead_midrow_notes: 657
- lead_highrow_notes: 53
- support_notes_pruned: 128
- chromatic_tokens: 605
