# Analysis (Yihuan 36-Key Ballad36 Script): Rush_E.mid

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
- octave_windows: w00-w38:+0
- lead_notes: 835
- lead_from_melody_track: 768 (92.0%)
- lead_from_top_note: 821 (98.3%)
- fallback_lead_notes: 67
- lead_midlead_moved: 290
- lead_midrow_notes: 488
- lead_highrow_notes: 55
- lead_ornaments_dropped: 23
- support_notes_pruned: 12
- chromatic_tokens: 207
