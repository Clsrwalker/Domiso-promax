# Analysis (Yihuan 36-Key MidLead36 Script): night-dancer-imase.mid

## Metrics
- note_count: 1787
- duration_s: 210.0547201448854
- tempo0: 117
- tempo_events: 5
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.693069306930692
- bar_density_p90: 24.8
- tracks: 2
- pitch_min: 29
- pitch_max: 89

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
- octave_windows: w00-w25:+0
- lead_notes: 674
- lead_from_melody_track: 631 (93.6%)
- lead_from_top_note: 673 (99.9%)
- fallback_lead_notes: 43
- lead_midlead_moved: 286
- lead_midrow_notes: 491
- lead_highrow_notes: 105
- support_notes_pruned: 26
- chromatic_tokens: 496
