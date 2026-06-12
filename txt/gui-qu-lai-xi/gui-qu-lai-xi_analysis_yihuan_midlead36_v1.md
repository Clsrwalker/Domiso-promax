# Analysis (Yihuan 36-Key MidLead36 Script): gui-qu-lai-xi.mid

## Metrics
- note_count: 734
- duration_s: 175.28571428571428
- tempo0: 70
- tempo_events: 1
- time_sig: 1/8
- max_poly: 5
- bar_density_mean: 1.8258706467661692
- bar_density_p90: 3.0
- tracks: 2
- pitch_min: 24
- pitch_max: 86

## Recommended Profile
- yihuan_midlead36
- reason: default Yihuan 36-key midlead36 profile

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
- octave_windows: w00-w12:+0
- lead_notes: 286
- lead_from_melody_track: 284 (99.3%)
- lead_from_top_note: 286 (100.0%)
- fallback_lead_notes: 2
- lead_midlead_moved: 201
- lead_midrow_notes: 222
- lead_highrow_notes: 15
- support_notes_pruned: 0
- chromatic_tokens: 202
