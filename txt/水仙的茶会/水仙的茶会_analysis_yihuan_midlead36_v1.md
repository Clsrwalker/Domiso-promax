# Analysis (Yihuan 36-Key MidLead36 Script): 水仙的茶会.mid

## Metrics
- note_count: 396
- duration_s: 117.69711538461537
- tempo0: 52
- tempo_events: 2
- time_sig: 6/8
- max_poly: 5
- bar_density_mean: 12.0
- bar_density_p90: 16.6
- tracks: 2
- pitch_min: 52
- pitch_max: 93

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
- octave_windows: w00-w06:-12
- lead_notes: 190
- lead_from_melody_track: 168 (88.4%)
- lead_from_top_note: 190 (100.0%)
- fallback_lead_notes: 22
- lead_midlead_moved: 46
- lead_midrow_notes: 169
- lead_highrow_notes: 6
- support_notes_pruned: 0
- chromatic_tokens: 107
