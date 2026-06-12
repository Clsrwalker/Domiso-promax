# Analysis (Yihuan 36-Key LowLead36 Script): all-of-me-violin.mid

## Metrics
- note_count: 464
- duration_s: 264.0
- tempo0: 120
- tempo_events: 1
- time_sig: 2/2
- max_poly: 1
- bar_density_mean: 3.515151515151515
- bar_density_p90: 5.0
- tracks: 1
- pitch_min: 56
- pitch_max: 77

## Recommended Profile
- yihuan_lowlead36
- reason: default Yihuan 36-key lowlead36 profile

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
- octave_windows: w00-w32:+0
- lead_notes: 464
- lead_from_melody_track: 464 (100.0%)
- lead_from_top_note: 464 (100.0%)
- fallback_lead_notes: 0
- lead_lowlead_moved: 237
- lead_lowrow_notes: 257
- lead_midrow_notes: 99
- lead_highrow_notes: 0
- lead_ornaments_dropped: 0
- support_notes_pruned: 0
- chromatic_tokens: 246
