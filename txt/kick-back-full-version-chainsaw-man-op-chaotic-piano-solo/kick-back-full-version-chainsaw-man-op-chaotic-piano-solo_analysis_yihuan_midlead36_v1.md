# Analysis (Yihuan 36-Key MidLead36 Script): kick-back-full-version-chainsaw-man-op-chaotic-piano-solo.mid

## Metrics
- note_count: 3136
- duration_s: 197.94753228685258
- tempo0: 102
- tempo_events: 9
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 37.78313253012048
- bar_density_p90: 58.6
- tracks: 2
- pitch_min: 25
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
- lead_notes: 808
- lead_from_melody_track: 781 (96.7%)
- lead_from_top_note: 800 (99.0%)
- fallback_lead_notes: 27
- lead_midlead_moved: 446
- lead_midrow_notes: 571
- lead_highrow_notes: 43
- support_notes_pruned: 124
- chromatic_tokens: 1428
