# Analysis (Yihuan 36-Key Ballad36 Script): ni-de-bei-bao.mid

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
- yihuan_ballad36_dense
- reason: dense piano texture -> yihuan_ballad36_dense

## Yihuan 36-Key Ballad36 Intent
- prioritize a singable vocal-like lead over piano figurations
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A in the middle row whenever possible and smooth out tiny ornament notes
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- simplify accompaniment into soft harmonic pads and bass anchors
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 12
- octave_windows: w00-w14:+12
- lead_notes: 433
- lead_from_melody_track: 412 (95.2%)
- lead_from_top_note: 413 (95.4%)
- fallback_lead_notes: 21
- lead_midlead_moved: 293
- lead_midrow_notes: 322
- lead_highrow_notes: 8
- lead_ornaments_dropped: 38
- support_notes_pruned: 440
- chromatic_tokens: 345
