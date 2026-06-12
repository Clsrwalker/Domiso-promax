# Analysis (Yihuan 36-Key MidLead36 Script): g-minor-bach.mid

## Metrics
- note_count: 1810
- duration_s: 158.28
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 27.424242424242426
- bar_density_p90: 34.0
- tracks: 3
- pitch_min: 34
- pitch_max: 80

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
- octave_windows: w00-w16:+0
- lead_notes: 365
- lead_from_melody_track: 8 (2.2%)
- lead_from_top_note: 365 (100.0%)
- fallback_lead_notes: 357
- lead_midlead_moved: 129
- lead_midrow_notes: 323
- lead_highrow_notes: 18
- support_notes_pruned: 1
- chromatic_tokens: 583
