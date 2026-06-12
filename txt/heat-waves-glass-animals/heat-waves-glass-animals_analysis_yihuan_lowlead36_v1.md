# Analysis (Yihuan 36-Key LowLead36 Script): heat-waves-glass-animals.mid

## Metrics
- note_count: 1593
- duration_s: 219.08333333333331
- tempo0: 81
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 21.82191780821918
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 28
- pitch_max: 87

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
- base_shift: 12
- octave_windows: w00-w18:+12
- lead_notes: 652
- lead_from_melody_track: 595 (91.3%)
- lead_from_top_note: 631 (96.8%)
- fallback_lead_notes: 57
- lead_lowlead_moved: 419
- lead_lowrow_notes: 396
- lead_midrow_notes: 55
- lead_highrow_notes: 0
- lead_ornaments_dropped: 16
- support_notes_pruned: 657
- chromatic_tokens: 361
