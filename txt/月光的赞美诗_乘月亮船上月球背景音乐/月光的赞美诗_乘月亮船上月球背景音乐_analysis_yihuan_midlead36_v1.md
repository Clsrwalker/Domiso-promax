# Analysis (Yihuan 36-Key MidLead36 Script): 月光的赞美诗_乘月亮船上月球背景音乐.mid

## Metrics
- note_count: 1054
- duration_s: 193.29427083333334
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 11.094736842105263
- bar_density_p90: 17.0
- tracks: 2
- pitch_min: 34
- pitch_max: 101

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
- octave_windows: w00-w23:+0
- lead_notes: 431
- lead_from_melody_track: 399 (92.6%)
- lead_from_top_note: 431 (100.0%)
- fallback_lead_notes: 32
- lead_midlead_moved: 299
- lead_midrow_notes: 381
- lead_highrow_notes: 22
- support_notes_pruned: 64
- chromatic_tokens: 417
