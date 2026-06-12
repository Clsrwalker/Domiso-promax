# Analysis (Yihuan 36-Key MidLead36 Script): hou-lai.mid

## Metrics
- note_count: 1465
- duration_s: 316.8
- tempo0: 75
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 14.797979797979798
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 24
- pitch_max: 98

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
- octave_windows: w00-w24:+0
- lead_notes: 567
- lead_from_melody_track: 542 (95.6%)
- lead_from_top_note: 567 (100.0%)
- fallback_lead_notes: 25
- lead_midlead_moved: 376
- lead_midrow_notes: 443
- lead_highrow_notes: 11
- support_notes_pruned: 0
- chromatic_tokens: 700
