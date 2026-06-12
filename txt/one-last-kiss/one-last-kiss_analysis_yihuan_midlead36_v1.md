# Analysis (Yihuan 36-Key MidLead36 Script): one-last-kiss.mid

## Metrics
- note_count: 2095
- duration_s: 246.9494494047619
- tempo0: 112
- tempo_events: 4
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 18.37719298245614
- bar_density_p90: 27.0
- tracks: 2
- pitch_min: 37
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
- octave_windows: w00-w28:+0
- lead_notes: 790
- lead_from_melody_track: 776 (98.2%)
- lead_from_top_note: 790 (100.0%)
- fallback_lead_notes: 14
- lead_midlead_moved: 405
- lead_midrow_notes: 536
- lead_highrow_notes: 16
- support_notes_pruned: 33
- chromatic_tokens: 1262
