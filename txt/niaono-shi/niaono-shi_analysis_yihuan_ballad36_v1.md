# Analysis (Yihuan 36-Key Ballad36 Script): niaono-shi.mid

## Metrics
- note_count: 3718
- duration_s: 374.7561475409836
- tempo0: 122
- tempo_events: 2
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 19.77659574468085
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 27
- pitch_max: 95

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
- octave_windows: w00-w46:+0
- lead_notes: 1044
- lead_from_melody_track: 962 (92.1%)
- lead_from_top_note: 771 (73.9%)
- fallback_lead_notes: 82
- lead_midlead_moved: 433
- lead_midrow_notes: 865
- lead_highrow_notes: 58
- lead_ornaments_dropped: 51
- support_notes_pruned: 382
- chromatic_tokens: 1003
