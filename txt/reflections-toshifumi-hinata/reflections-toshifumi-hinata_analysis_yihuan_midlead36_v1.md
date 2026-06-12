# Analysis (Yihuan 36-Key MidLead36 Script): reflections-toshifumi-hinata.mid

## Metrics
- note_count: 1107
- duration_s: 200.77043269230768
- tempo0: 104
- tempo_events: 1
- time_sig: 3/4
- max_poly: 6
- bar_density_mean: 9.626086956521739
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 26
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
- base_shift: 12
- octave_windows: w00-w21:+12
- lead_notes: 363
- lead_from_melody_track: 334 (92.0%)
- lead_from_top_note: 363 (100.0%)
- fallback_lead_notes: 29
- lead_midlead_moved: 212
- lead_midrow_notes: 298
- lead_highrow_notes: 14
- support_notes_pruned: 7
- chromatic_tokens: 30
