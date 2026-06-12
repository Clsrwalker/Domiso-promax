# Analysis (Yihuan 36-Key MidLead36 Script): windakeboshi-naruto-ed01.mid

## Metrics
- note_count: 1647
- duration_s: 195.9715909090909
- tempo0: 88
- tempo_events: 1
- time_sig: 5/8
- max_poly: 6
- bar_density_mean: 14.321739130434782
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 36
- pitch_max: 86

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
- octave_windows: w00-w17:+0
- lead_notes: 468
- lead_from_melody_track: 462 (98.7%)
- lead_from_top_note: 468 (100.0%)
- fallback_lead_notes: 6
- lead_midlead_moved: 154
- lead_midrow_notes: 335
- lead_highrow_notes: 37
- support_notes_pruned: 9
- chromatic_tokens: 701
