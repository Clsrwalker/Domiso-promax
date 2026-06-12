# Analysis (Yihuan 36-Key MidLead36 Script): Rush_E.mid

## Metrics
- note_count: 1842
- duration_s: 179.43580538189738
- tempo0: 70
- tempo_events: 186
- time_sig: 4/4
- max_poly: 57
- bar_density_mean: 11.883870967741936
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 25
- pitch_max: 108

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
- octave_windows: w00-w38:+0
- lead_notes: 835
- lead_from_melody_track: 768 (92.0%)
- lead_from_top_note: 835 (100.0%)
- fallback_lead_notes: 67
- lead_midlead_moved: 294
- lead_midrow_notes: 488
- lead_highrow_notes: 55
- support_notes_pruned: 9
- chromatic_tokens: 228
