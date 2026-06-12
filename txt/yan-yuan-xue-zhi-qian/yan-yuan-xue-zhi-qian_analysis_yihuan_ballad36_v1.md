# Analysis (Yihuan 36-Key Ballad36 Script): yan-yuan-xue-zhi-qian.mid

## Metrics
- note_count: 896
- duration_s: 132.2400442477876
- tempo0: 120
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.575757575757576
- bar_density_p90: 20.3
- tracks: 2
- pitch_min: 16
- pitch_max: 102

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
- octave_windows: w00-w16:+0
- lead_notes: 390
- lead_from_melody_track: 377 (96.7%)
- lead_from_top_note: 341 (87.4%)
- fallback_lead_notes: 13
- lead_midlead_moved: 169
- lead_midrow_notes: 277
- lead_highrow_notes: 29
- lead_ornaments_dropped: 4
- support_notes_pruned: 58
- chromatic_tokens: 430
