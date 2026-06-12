# Analysis (Yihuan 36-Key LowLead36 Script): night-dancer-imase.mid

## Metrics
- note_count: 1787
- duration_s: 210.0547201448854
- tempo0: 117
- tempo_events: 5
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.693069306930692
- bar_density_p90: 24.8
- tracks: 2
- pitch_min: 29
- pitch_max: 89

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
- octave_windows: w00-w25:+0
- lead_notes: 652
- lead_from_melody_track: 631 (96.8%)
- lead_from_top_note: 574 (88.0%)
- fallback_lead_notes: 21
- lead_lowlead_moved: 506
- lead_lowrow_notes: 416
- lead_midrow_notes: 144
- lead_highrow_notes: 0
- lead_ornaments_dropped: 4
- support_notes_pruned: 461
- chromatic_tokens: 282
