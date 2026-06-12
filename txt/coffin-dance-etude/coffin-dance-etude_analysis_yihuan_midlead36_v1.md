# Analysis (Yihuan 36-Key MidLead36 Script): coffin-dance-etude.mid

## Metrics
- note_count: 2230
- duration_s: 117.50086805555557
- tempo0: 144
- tempo_events: 1
- time_sig: 2/4
- max_poly: 5
- bar_density_mean: 15.815602836879433
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 22
- pitch_max: 103

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
- octave_windows: w00-w17:+0
- lead_notes: 805
- lead_from_melody_track: 789 (98.0%)
- lead_from_top_note: 805 (100.0%)
- fallback_lead_notes: 16
- lead_midlead_moved: 541
- lead_midrow_notes: 613
- lead_highrow_notes: 9
- support_notes_pruned: 153
- chromatic_tokens: 454
