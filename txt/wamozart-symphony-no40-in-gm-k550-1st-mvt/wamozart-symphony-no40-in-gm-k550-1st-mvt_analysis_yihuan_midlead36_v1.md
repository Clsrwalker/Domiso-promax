# Analysis (Yihuan 36-Key MidLead36 Script): wamozart-symphony-no40-in-gm-k550-1st-mvt.mid

## Metrics
- note_count: 5533
- duration_s: 455.4
- tempo0: 210
- tempo_events: 1
- time_sig: 2/2
- max_poly: 7
- bar_density_mean: 13.867167919799499
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 36
- pitch_max: 91

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
- octave_windows: w00-w99:+0
- lead_notes: 2294
- lead_from_melody_track: 2015 (87.8%)
- lead_from_top_note: 2222 (96.9%)
- fallback_lead_notes: 279
- lead_midlead_moved: 1271
- lead_midrow_notes: 1900
- lead_highrow_notes: 95
- support_notes_pruned: 37
- chromatic_tokens: 1913
