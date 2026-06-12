# Analysis (Yihuan 36-Key MidLead36 Script): sis-puella-magica-puella-magi-madoka-magica-yuki-kajiura.mid

## Metrics
- note_count: 1386
- duration_s: 189.5
- tempo0: 120
- tempo_events: 1
- time_sig: 3/4
- max_poly: 9
- bar_density_mean: 11.0
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 27
- pitch_max: 87

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
- lead_notes: 414
- lead_from_melody_track: 392 (94.7%)
- lead_from_top_note: 414 (100.0%)
- fallback_lead_notes: 22
- lead_midlead_moved: 223
- lead_midrow_notes: 353
- lead_highrow_notes: 23
- support_notes_pruned: 18
- chromatic_tokens: 344
