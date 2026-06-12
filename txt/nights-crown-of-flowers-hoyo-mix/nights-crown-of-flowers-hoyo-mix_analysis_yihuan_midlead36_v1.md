# Analysis (Yihuan 36-Key MidLead36 Script): nights-crown-of-flowers-hoyo-mix.mid

## Metrics
- note_count: 742
- duration_s: 119.14285714285714
- tempo0: 140
- tempo_events: 1
- time_sig: 6/4
- max_poly: 6
- bar_density_mean: 16.130434782608695
- bar_density_p90: 21.3
- tracks: 2
- pitch_min: 35
- pitch_max: 86

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
- lead_notes: 358
- lead_from_melody_track: 340 (95.0%)
- lead_from_top_note: 355 (99.2%)
- fallback_lead_notes: 18
- lead_midlead_moved: 147
- lead_midrow_notes: 317
- lead_highrow_notes: 4
- support_notes_pruned: 5
- chromatic_tokens: 271
