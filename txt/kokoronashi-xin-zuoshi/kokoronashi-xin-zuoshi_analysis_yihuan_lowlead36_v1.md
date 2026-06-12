# Analysis (Yihuan 36-Key LowLead36 Script): kokoronashi-xin-zuoshi.mid

## Metrics
- note_count: 1978
- duration_s: 395.4170256079848
- tempo0: 76
- tempo_events: 35
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 21.268817204301076
- bar_density_p90: 35.0
- tracks: 2
- pitch_min: 26
- pitch_max: 93

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
- octave_windows: w00-w23:+0
- lead_notes: 850
- lead_from_melody_track: 735 (86.5%)
- lead_from_top_note: 816 (96.0%)
- fallback_lead_notes: 115
- lead_lowlead_moved: 613
- lead_lowrow_notes: 641
- lead_midrow_notes: 99
- lead_highrow_notes: 0
- lead_ornaments_dropped: 38
- support_notes_pruned: 600
- chromatic_tokens: 198
