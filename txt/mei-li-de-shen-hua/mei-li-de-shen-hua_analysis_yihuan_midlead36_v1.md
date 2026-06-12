# Analysis (Yihuan 36-Key MidLead36 Script): mei-li-de-shen-hua.mid

## Metrics
- note_count: 1820
- duration_s: 314.0
- tempo0: 60
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 23.636363636363637
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 29
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
- octave_windows: w00-w19:+0
- lead_notes: 471
- lead_from_melody_track: 462 (98.1%)
- lead_from_top_note: 468 (99.4%)
- fallback_lead_notes: 9
- lead_midlead_moved: 207
- lead_midrow_notes: 384
- lead_highrow_notes: 43
- support_notes_pruned: 93
- chromatic_tokens: 420
