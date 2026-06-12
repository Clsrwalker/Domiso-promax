# Analysis (Yihuan 36-Key Restore36 Script): ni-de-bei-bao.mid

## Metrics
- note_count: 1325
- duration_s: 205.53214285714284
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 22.45762711864407
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 25
- pitch_max: 88

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
- octave_windows: w00-w14:+12
- lead_notes: 437
- lead_from_melody_track: 412 (94.3%)
- lead_from_top_note: 437 (100.0%)
- fallback_lead_notes: 25
- support_notes_pruned: 11
- chromatic_tokens: 625
