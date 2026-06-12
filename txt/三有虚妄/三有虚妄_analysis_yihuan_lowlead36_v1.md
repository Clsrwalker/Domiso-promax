# Analysis (Yihuan 36-Key LowLead36 Script): 三有虚妄.mid

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
- yihuan_lowlead36_dense
- reason: dense piano texture -> yihuan_lowlead36_dense

## Yihuan 36-Key LowLead36 Intent
- prioritize a recognizable low-register lead over piano figurations
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A mostly in the low row C3-B3 (Z X C V B N M) and smooth out tiny ornament notes
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- simplify accompaniment into sparse upper support and occasional bass anchors
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 0
- octave_windows: w00-w05:+0
- lead_notes: 135
- lead_from_melody_track: 134 (99.3%)
- lead_from_top_note: 127 (94.1%)
- fallback_lead_notes: 1
- lead_lowlead_moved: 81
- lead_lowrow_notes: 110
- lead_midrow_notes: 8
- lead_highrow_notes: 0
- lead_ornaments_dropped: 4
- support_notes_pruned: 186
- chromatic_tokens: 35
