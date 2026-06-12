# Analysis (Yihuan 36-Key MidLead36 Script): 【ff14】銀色飛行船.mid

## Metrics
- note_count: 1836
- duration_s: 420.85714285714283
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 15.692307692307692
- bar_density_p90: 24.0
- tracks: 1
- pitch_min: 27
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
- octave_windows: w00-w29:+0
- lead_notes: 932
- lead_from_melody_track: 932 (100.0%)
- lead_from_top_note: 932 (100.0%)
- fallback_lead_notes: 0
- lead_midlead_moved: 470
- lead_midrow_notes: 756
- lead_highrow_notes: 47
- support_notes_pruned: 0
- chromatic_tokens: 806
