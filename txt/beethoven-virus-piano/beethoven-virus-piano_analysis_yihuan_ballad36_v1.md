# Analysis (Yihuan 36-Key Ballad36 Script): beethoven-virus-piano.mid

## Metrics
- note_count: 2671
- duration_s: 216.73125
- tempo0: 160
- tempo_events: 3
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.07857142857143
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 21
- pitch_max: 100

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
- octave_windows: w00-w34:+0
- lead_notes: 1069
- lead_from_melody_track: 1012 (94.7%)
- lead_from_top_note: 961 (89.9%)
- fallback_lead_notes: 57
- lead_midlead_moved: 580
- lead_midrow_notes: 881
- lead_highrow_notes: 99
- lead_ornaments_dropped: 109
- support_notes_pruned: 293
- chromatic_tokens: 251
