# Analysis (Yihuan 36-Key MidLead36 Script): moonlight-sonata-3rd-movement.mid

## Metrics
- note_count: 6414
- duration_s: 374.8058823529412
- tempo0: 170
- tempo_events: 3
- time_sig: 4/4
- max_poly: 10
- bar_density_mean: 24.295454545454547
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 29
- pitch_max: 88

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
- octave_windows: w00-w65:+0
- lead_notes: 2385
- lead_from_melody_track: 2283 (95.7%)
- lead_from_top_note: 2385 (100.0%)
- fallback_lead_notes: 102
- lead_midlead_moved: 1092
- lead_midrow_notes: 1929
- lead_highrow_notes: 151
- support_notes_pruned: 865
- chromatic_tokens: 3128
