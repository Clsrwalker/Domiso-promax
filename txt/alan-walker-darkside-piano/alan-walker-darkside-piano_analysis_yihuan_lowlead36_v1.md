# Analysis (Yihuan 36-Key LowLead36 Script): alan-walker-darkside-piano.mid

## Metrics
- note_count: 1341
- duration_s: 217.34117647058824
- tempo0: 170
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 8.707792207792208
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 36
- pitch_max: 84

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
- base_shift: 12
- octave_windows: w00-w38:+12
- lead_notes: 442
- lead_from_melody_track: 416 (94.1%)
- lead_from_top_note: 426 (96.4%)
- fallback_lead_notes: 26
- lead_lowlead_moved: 392
- lead_lowrow_notes: 391
- lead_midrow_notes: 5
- lead_highrow_notes: 0
- lead_ornaments_dropped: 10
- support_notes_pruned: 692
- chromatic_tokens: 62
