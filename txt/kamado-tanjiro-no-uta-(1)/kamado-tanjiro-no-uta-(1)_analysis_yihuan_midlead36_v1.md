# Analysis (Yihuan 36-Key MidLead36 Script): kamado-tanjiro-no-uta (1).mid

## Metrics
- note_count: 646
- duration_s: 74.87583333333333
- tempo0: 150
- tempo_events: 3
- time_sig: 1/4
- max_poly: 8
- bar_density_mean: 3.530054644808743
- bar_density_p90: 6.0
- tracks: 2
- pitch_min: 29
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
- octave_windows: w00-w11:+0
- lead_notes: 163
- lead_from_melody_track: 162 (99.4%)
- lead_from_top_note: 162 (99.4%)
- fallback_lead_notes: 1
- lead_midlead_moved: 101
- lead_midrow_notes: 142
- lead_highrow_notes: 3
- support_notes_pruned: 83
- chromatic_tokens: 63
