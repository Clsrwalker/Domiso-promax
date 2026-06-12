# Analysis (Yihuan 36-Key MidLead36 Script): kokoronashi-xin-zuoshi.mid

## Metrics
- note_count: 1978
- duration_s: 395.4170256079848
- tempo0: 76
- tempo_events: 35
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 21.268817204301076
- bar_density_p90: 35.0
- tracks: 2
- pitch_min: 26
- pitch_max: 93

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
- lead_notes: 858
- lead_from_melody_track: 735 (85.7%)
- lead_from_top_note: 856 (99.8%)
- fallback_lead_notes: 123
- lead_midlead_moved: 578
- lead_midrow_notes: 733
- lead_highrow_notes: 17
- support_notes_pruned: 61
- chromatic_tokens: 496
