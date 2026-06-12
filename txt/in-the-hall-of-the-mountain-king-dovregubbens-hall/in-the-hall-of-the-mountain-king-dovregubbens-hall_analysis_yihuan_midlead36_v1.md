# Analysis (Yihuan 36-Key MidLead36 Script): in-the-hall-of-the-mountain-king-dovregubbens-hall.mid

## Metrics
- note_count: 1430
- duration_s: 143.00652173913042
- tempo0: 138
- tempo_events: 4
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 16.25
- bar_density_p90: 22.2
- tracks: 2
- pitch_min: 23
- pitch_max: 99

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
- octave_windows: w00-w21:+0
- lead_notes: 560
- lead_from_melody_track: 516 (92.1%)
- lead_from_top_note: 560 (100.0%)
- fallback_lead_notes: 44
- lead_midlead_moved: 446
- lead_midrow_notes: 528
- lead_highrow_notes: 14
- support_notes_pruned: 34
- chromatic_tokens: 628
