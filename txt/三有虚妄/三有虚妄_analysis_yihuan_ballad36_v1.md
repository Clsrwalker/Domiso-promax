# Analysis (Yihuan 36-Key Ballad36 Script): 三有虚妄.mid

## Metrics
- note_count: 376
- duration_s: 91.89526936174494
- tempo0: 65
- tempo_events: 5
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 11.75
- bar_density_p90: 18.7
- tracks: 2
- pitch_min: 40
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
- octave_windows: w00-w05:+0
- lead_notes: 135
- lead_from_melody_track: 134 (99.3%)
- lead_from_top_note: 118 (87.4%)
- fallback_lead_notes: 1
- lead_midlead_moved: 32
- lead_midrow_notes: 85
- lead_highrow_notes: 4
- lead_ornaments_dropped: 3
- support_notes_pruned: 2
- chromatic_tokens: 65
