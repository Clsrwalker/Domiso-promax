# Analysis (Yihuan 36-Key MidLead36 Script): 如生之不竭.mid

## Metrics
- note_count: 1562
- duration_s: 151.69811320754715
- tempo0: 106
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 23.313432835820894
- bar_density_p90: 33.4
- tracks: 2
- pitch_min: 38
- pitch_max: 95

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
- lead_notes: 699
- lead_from_melody_track: 667 (95.4%)
- lead_from_top_note: 699 (100.0%)
- fallback_lead_notes: 32
- lead_midlead_moved: 542
- lead_midrow_notes: 600
- lead_highrow_notes: 13
- support_notes_pruned: 86
- chromatic_tokens: 49
