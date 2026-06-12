# Analysis (Yihuan 36-Key MidLead36 Script): fragile-fantasy-genshin-impact-dragonspine-ost-3-piano-solo.mid

## Metrics
- note_count: 349
- duration_s: 115.86206896551725
- tempo0: 58
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 12.464285714285714
- bar_density_p90: 20.1
- tracks: 2
- pitch_min: 39
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
- octave_windows: w00-w06:+0
- lead_notes: 155
- lead_from_melody_track: 133 (85.8%)
- lead_from_top_note: 155 (100.0%)
- fallback_lead_notes: 22
- lead_midlead_moved: 107
- lead_midrow_notes: 139
- lead_highrow_notes: 6
- support_notes_pruned: 0
- chromatic_tokens: 72
