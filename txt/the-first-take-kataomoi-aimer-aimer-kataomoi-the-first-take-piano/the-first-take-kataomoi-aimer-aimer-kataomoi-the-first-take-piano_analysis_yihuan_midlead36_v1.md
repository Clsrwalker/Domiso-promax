# Analysis (Yihuan 36-Key MidLead36 Script): the-first-take-kataomoi-aimer-aimer-kataomoi-the-first-take-piano.mid

## Metrics
- note_count: 1282
- duration_s: 205.36082474226805
- tempo0: 97
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 15.44578313253012
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 30
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
- octave_windows: w00-w20:+0
- lead_notes: 476
- lead_from_melody_track: 455 (95.6%)
- lead_from_top_note: 475 (99.8%)
- fallback_lead_notes: 21
- lead_midlead_moved: 202
- lead_midrow_notes: 386
- lead_highrow_notes: 43
- support_notes_pruned: 28
- chromatic_tokens: 1000
