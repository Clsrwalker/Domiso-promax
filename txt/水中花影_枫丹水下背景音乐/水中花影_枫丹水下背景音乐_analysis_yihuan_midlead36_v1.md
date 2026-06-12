# Analysis (Yihuan 36-Key MidLead36 Script): 水中花影_枫丹水下背景音乐.mid

## Metrics
- note_count: 400
- duration_s: 75.871875
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 10.81081081081081
- bar_density_p90: 14.0
- tracks: 2
- pitch_min: 48
- pitch_max: 86

## Recommended Profile
- yihuan_midlead36
- reason: default Yihuan 36-key midlead36 profile

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
- octave_windows: w00-w09:+0
- lead_notes: 264
- lead_from_melody_track: 215 (81.4%)
- lead_from_top_note: 264 (100.0%)
- fallback_lead_notes: 49
- lead_midlead_moved: 128
- lead_midrow_notes: 248
- lead_highrow_notes: 1
- support_notes_pruned: 17
- chromatic_tokens: 53
