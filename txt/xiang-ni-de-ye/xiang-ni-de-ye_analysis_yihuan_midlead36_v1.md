# Analysis (Yihuan 36-Key MidLead36 Script): xiang-ni-de-ye.mid

## Metrics
- note_count: 476
- duration_s: 127.17857142857142
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 12.864864864864865
- bar_density_p90: 16.2
- tracks: 2
- pitch_min: 41
- pitch_max: 89

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
- lead_notes: 226
- lead_from_melody_track: 213 (94.2%)
- lead_from_top_note: 226 (100.0%)
- fallback_lead_notes: 13
- lead_midlead_moved: 127
- lead_midrow_notes: 183
- lead_highrow_notes: 12
- support_notes_pruned: 0
- chromatic_tokens: 70
