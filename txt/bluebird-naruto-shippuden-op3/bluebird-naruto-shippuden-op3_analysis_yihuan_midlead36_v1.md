# Analysis (Yihuan 36-Key MidLead36 Script): bluebird-naruto-shippuden-op3.mid

## Metrics
- note_count: 1019
- duration_s: 69.378125
- tempo0: 80
- tempo_events: 1
- time_sig: 5/4
- max_poly: 8
- bar_density_mean: 53.63157894736842
- bar_density_p90: 95.0
- tracks: 2
- pitch_min: 35
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
- octave_windows: w00-w05:+0
- lead_notes: 218
- lead_from_melody_track: 188 (86.2%)
- lead_from_top_note: 214 (98.2%)
- fallback_lead_notes: 30
- lead_midlead_moved: 157
- lead_midrow_notes: 179
- lead_highrow_notes: 16
- support_notes_pruned: 64
- chromatic_tokens: 318
