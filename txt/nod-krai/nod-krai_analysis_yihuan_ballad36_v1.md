# Analysis (Yihuan 36-Key Ballad36 Script): nod-krai.mid

## Metrics
- note_count: 2539
- duration_s: 254.90157128257536
- tempo0: 76
- tempo_events: 2
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 24.650485436893202
- bar_density_p90: 38.0
- tracks: 2
- pitch_min: 21
- pitch_max: 99

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
- base_shift: 0
- octave_windows: w00-w25:+0
- lead_notes: 712
- lead_from_melody_track: 707 (99.3%)
- lead_from_top_note: 523 (73.5%)
- fallback_lead_notes: 5
- lead_midlead_moved: 237
- lead_midrow_notes: 556
- lead_highrow_notes: 55
- lead_ornaments_dropped: 73
- support_notes_pruned: 513
- chromatic_tokens: 447
