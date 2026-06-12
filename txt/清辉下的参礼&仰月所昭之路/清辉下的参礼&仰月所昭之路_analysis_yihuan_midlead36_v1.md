# Analysis (Yihuan 36-Key MidLead36 Script): 清辉下的参礼&仰月所昭之路.mid

## Metrics
- note_count: 587
- duration_s: 121.76410495015617
- tempo0: 60
- tempo_events: 7
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 16.305555555555557
- bar_density_p90: 23.0
- tracks: 2
- pitch_min: 39
- pitch_max: 89

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
- octave_windows: w00-w08:+0
- lead_notes: 212
- lead_from_melody_track: 201 (94.8%)
- lead_from_top_note: 212 (100.0%)
- fallback_lead_notes: 11
- lead_midlead_moved: 170
- lead_midrow_notes: 199
- lead_highrow_notes: 7
- support_notes_pruned: 0
- chromatic_tokens: 67
