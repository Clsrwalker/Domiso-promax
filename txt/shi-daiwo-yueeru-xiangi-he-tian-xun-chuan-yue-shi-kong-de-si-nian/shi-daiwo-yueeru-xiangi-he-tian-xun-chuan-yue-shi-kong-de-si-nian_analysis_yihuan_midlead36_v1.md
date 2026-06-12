# Analysis (Yihuan 36-Key MidLead36 Script): shi-daiwo-yueeru-xiangi-he-tian-xun-chuan-yue-shi-kong-de-si-nian.mid

## Metrics
- note_count: 601
- duration_s: 140.0399646451867
- tempo0: 65
- tempo_events: 8
- time_sig: 2/4
- max_poly: 6
- bar_density_mean: 8.464788732394366
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 27
- pitch_max: 96

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
- octave_windows: w00-w08:+0
- lead_notes: 171
- lead_from_melody_track: 166 (97.1%)
- lead_from_top_note: 170 (99.4%)
- fallback_lead_notes: 5
- lead_midlead_moved: 145
- lead_midrow_notes: 161
- lead_highrow_notes: 3
- support_notes_pruned: 35
- chromatic_tokens: 89
