# Analysis (Yihuan 36-Key MidLead36 Script): xin-ru-zhi-shui-ice-paper.mid

## Metrics
- note_count: 1466
- duration_s: 182.85714285714283
- tempo0: 126
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 15.270833333333334
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 44
- pitch_max: 82

## Recommended Profile
- yihuan_midlead36_dense
- reason: dense piano texture -> yihuan_midlead36_dense

## Yihuan 36-Key MidLead36 Intent
- preserve literal rhythm/body more aggressively than melodylock
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A as the lead anchor and prefer the middle row C4-B4
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- retain more source harmony in B/C than melodylock
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 0
- octave_windows: w00-w23:+0
- lead_notes: 757
- lead_from_melody_track: 728 (96.2%)
- lead_from_top_note: 752 (99.3%)
- fallback_lead_notes: 29
- lead_midlead_moved: 256
- lead_midrow_notes: 587
- lead_highrow_notes: 24
- support_notes_pruned: 6
- chromatic_tokens: 1351
