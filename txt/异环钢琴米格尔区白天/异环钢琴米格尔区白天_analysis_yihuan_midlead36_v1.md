# Analysis (Yihuan 36-Key MidLead36 Script): 异环钢琴米格尔区白天.mid

## Metrics
- note_count: 621
- duration_s: 176.34427083333333
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 7.22093023255814
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 41
- pitch_max: 94

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
- octave_windows: w00-w21:+0
- lead_notes: 273
- lead_from_melody_track: 242 (88.6%)
- lead_from_top_note: 273 (100.0%)
- fallback_lead_notes: 31
- lead_midlead_moved: 162
- lead_midrow_notes: 251
- lead_highrow_notes: 12
- support_notes_pruned: 36
- chromatic_tokens: 91
