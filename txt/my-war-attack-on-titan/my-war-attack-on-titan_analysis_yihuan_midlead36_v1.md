# Analysis (Yihuan 36-Key MidLead36 Script): my-war-attack-on-titan.mid

## Metrics
- note_count: 963
- duration_s: 86.64583333333333
- tempo0: 144
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 18.51923076923077
- bar_density_p90: 25.4
- tracks: 2
- pitch_min: 25
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
- octave_windows: w00-w12:+0
- lead_notes: 281
- lead_from_melody_track: 272 (96.8%)
- lead_from_top_note: 281 (100.0%)
- fallback_lead_notes: 9
- lead_midlead_moved: 147
- lead_midrow_notes: 174
- lead_highrow_notes: 7
- support_notes_pruned: 116
- chromatic_tokens: 413
