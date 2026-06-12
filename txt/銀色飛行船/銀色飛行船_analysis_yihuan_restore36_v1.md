# Analysis (Yihuan 36-Key Restore36 Script): 銀色飛行船.mid

## Metrics
- note_count: 932
- duration_s: 227.41544117647058
- tempo0: 68
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 14.338461538461539
- bar_density_p90: 23.4
- tracks: 5
- pitch_min: 37
- pitch_max: 77

## Recommended Profile
- yihuan_restore36_dense
- reason: dense piano texture -> yihuan_restore36_dense

## Yihuan 36-Key Restore36 Intent
- preserve literal rhythm/body more aggressively than melodylock
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A as the lead anchor but retain more source harmony in B/C
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 12
- octave_windows: w00-w16:+12
- lead_notes: 368
- lead_from_melody_track: 309 (84.0%)
- lead_from_top_note: 355 (96.5%)
- fallback_lead_notes: 59
- support_notes_pruned: 35
- chromatic_tokens: 507
