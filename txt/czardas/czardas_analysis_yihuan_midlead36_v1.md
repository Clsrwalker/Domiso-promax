# Analysis (Yihuan 36-Key MidLead36 Script): czardas.mid

## Metrics
- note_count: 2403
- duration_s: 268.61831376129766
- tempo0: 55
- tempo_events: 15
- time_sig: 2/4
- max_poly: 8
- bar_density_mean: 12.075376884422111
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 31
- pitch_max: 88

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
- octave_windows: w00-w24:+0
- lead_notes: 977
- lead_from_melody_track: 937 (95.9%)
- lead_from_top_note: 977 (100.0%)
- fallback_lead_notes: 40
- lead_midlead_moved: 684
- lead_midrow_notes: 870
- lead_highrow_notes: 41
- support_notes_pruned: 14
- chromatic_tokens: 406
