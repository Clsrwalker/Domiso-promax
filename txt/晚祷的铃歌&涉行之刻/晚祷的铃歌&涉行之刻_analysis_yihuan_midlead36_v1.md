# Analysis (Yihuan 36-Key MidLead36 Script): 晚祷的铃歌&涉行之刻.mid

## Metrics
- note_count: 534
- duration_s: 97.56896551724138
- tempo0: 120
- tempo_events: 2
- time_sig: 3/4
- max_poly: 3
- bar_density_mean: 8.215384615384615
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 48
- pitch_max: 88

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
- base_shift: -12
- octave_windows: w00-w12:-12
- lead_notes: 255
- lead_from_melody_track: 197 (77.3%)
- lead_from_top_note: 255 (100.0%)
- fallback_lead_notes: 58
- lead_midlead_moved: 108
- lead_midrow_notes: 222
- lead_highrow_notes: 15
- support_notes_pruned: 0
- chromatic_tokens: 10
