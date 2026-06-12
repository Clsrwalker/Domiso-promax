# Analysis (Yihuan 36-Key MidLead36 Script): persona-5-life-will-change-vocal-version.mid

## Metrics
- note_count: 2370
- duration_s: 265.68461538461537
- tempo0: 130
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 16.573426573426573
- bar_density_p90: 25.0
- tracks: 2
- pitch_min: 29
- pitch_max: 75

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
- base_shift: 12
- octave_windows: w00-w35:+12
- lead_notes: 839
- lead_from_melody_track: 725 (86.4%)
- lead_from_top_note: 839 (100.0%)
- fallback_lead_notes: 114
- lead_midlead_moved: 497
- lead_midrow_notes: 636
- lead_highrow_notes: 39
- support_notes_pruned: 4
- chromatic_tokens: 841
