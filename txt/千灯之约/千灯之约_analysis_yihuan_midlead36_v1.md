# Analysis (Yihuan 36-Key MidLead36 Script): 千灯之约.mid

## Metrics
- note_count: 1421
- duration_s: 329.75743402446193
- tempo0: 76
- tempo_events: 5
- time_sig: 6/8
- max_poly: 6
- bar_density_mean: 10.223021582733812
- bar_density_p90: 13.0
- tracks: 2
- pitch_min: 37
- pitch_max: 85

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
- octave_windows: w00-w25:+0
- lead_notes: 742
- lead_from_melody_track: 728 (98.1%)
- lead_from_top_note: 742 (100.0%)
- fallback_lead_notes: 14
- lead_midlead_moved: 184
- lead_midrow_notes: 558
- lead_highrow_notes: 73
- support_notes_pruned: 2
- chromatic_tokens: 1011
