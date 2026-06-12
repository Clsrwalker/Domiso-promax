# Analysis (Yihuan 36-Key MidLead36 Script): to-the-end-of-all-wars.mid

## Metrics
- note_count: 2910
- duration_s: 208.66071428571428
- tempo0: 112
- tempo_events: 1
- time_sig: 1/4
- max_poly: 12
- bar_density_mean: 7.461538461538462
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 21
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
- octave_windows: w00-w24:+0
- lead_notes: 896
- lead_from_melody_track: 871 (97.2%)
- lead_from_top_note: 890 (99.3%)
- fallback_lead_notes: 25
- lead_midlead_moved: 329
- lead_midrow_notes: 685
- lead_highrow_notes: 57
- support_notes_pruned: 99
- chromatic_tokens: 1355
