# Analysis (Yihuan 36-Key MidLead36 Script): kiss-the-rain-yiruma.mid

## Metrics
- note_count: 1052
- duration_s: 266.49997201074785
- tempo0: 63
- tempo_events: 8
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.701492537313433
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 33
- pitch_max: 97

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
- lead_notes: 394
- lead_from_melody_track: 392 (99.5%)
- lead_from_top_note: 394 (100.0%)
- fallback_lead_notes: 2
- lead_midlead_moved: 233
- lead_midrow_notes: 294
- lead_highrow_notes: 15
- support_notes_pruned: 6
- chromatic_tokens: 583
