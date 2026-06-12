# Analysis (Yihuan 36-Key MidLead36 Script): gang-hao-yu-jian-ni-li-yugang-li-yu-gang-gang-hao-yu-jian-ni-li-yu-gang.mid

## Metrics
- note_count: 1130
- duration_s: 190.1314935064935
- tempo0: 77
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 18.524590163934427
- bar_density_p90: 26.8
- tracks: 2
- pitch_min: 23
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
- octave_windows: w00-w15:+0
- lead_notes: 374
- lead_from_melody_track: 356 (95.2%)
- lead_from_top_note: 374 (100.0%)
- fallback_lead_notes: 18
- lead_midlead_moved: 189
- lead_midrow_notes: 266
- lead_highrow_notes: 22
- support_notes_pruned: 35
- chromatic_tokens: 688
