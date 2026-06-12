# Analysis (Yihuan 36-Key MidLead36 Script): 四不可说.mid

## Metrics
- note_count: 287
- duration_s: 88.88828321054527
- tempo0: 62
- tempo_events: 5
- time_sig: 3/4
- max_poly: 7
- bar_density_mean: 9.89655172413793
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 36
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
- octave_windows: w00-w05:+0
- lead_notes: 97
- lead_from_melody_track: 97 (100.0%)
- lead_from_top_note: 97 (100.0%)
- fallback_lead_notes: 0
- lead_midlead_moved: 62
- lead_midrow_notes: 72
- lead_highrow_notes: 1
- support_notes_pruned: 0
- chromatic_tokens: 122
