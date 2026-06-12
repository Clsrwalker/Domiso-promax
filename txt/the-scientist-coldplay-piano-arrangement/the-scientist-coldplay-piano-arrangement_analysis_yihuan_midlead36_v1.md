# Analysis (Yihuan 36-Key MidLead36 Script): the-scientist-coldplay-piano-arrangement.mid

## Metrics
- note_count: 1527
- duration_s: 291.16
- tempo0: 75
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 16.78021978021978
- bar_density_p90: 21.8
- tracks: 2
- pitch_min: 46
- pitch_max: 81

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
- lead_notes: 500
- lead_from_melody_track: 379 (75.8%)
- lead_from_top_note: 483 (96.6%)
- fallback_lead_notes: 121
- lead_midlead_moved: 78
- lead_midrow_notes: 362
- lead_highrow_notes: 25
- support_notes_pruned: 9
- chromatic_tokens: 64
