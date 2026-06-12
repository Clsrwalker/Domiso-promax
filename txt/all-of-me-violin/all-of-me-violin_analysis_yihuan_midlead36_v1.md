# Analysis (Yihuan 36-Key MidLead36 Script): all-of-me-violin.mid

## Metrics
- note_count: 464
- duration_s: 264.0
- tempo0: 120
- tempo_events: 1
- time_sig: 2/2
- max_poly: 1
- bar_density_mean: 3.515151515151515
- bar_density_p90: 5.0
- tracks: 1
- pitch_min: 56
- pitch_max: 77

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
- octave_windows: w00-w32:+0
- lead_notes: 464
- lead_from_melody_track: 464 (100.0%)
- lead_from_top_note: 464 (100.0%)
- fallback_lead_notes: 0
- lead_midlead_moved: 33
- lead_midrow_notes: 261
- lead_highrow_notes: 40
- support_notes_pruned: 0
- chromatic_tokens: 246
