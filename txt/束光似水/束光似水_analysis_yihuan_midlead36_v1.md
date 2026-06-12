# Analysis (Yihuan 36-Key MidLead36 Script): 束光似水.mid

## Metrics
- note_count: 132
- duration_s: 24.001041666666666
- tempo0: 120
- tempo_events: 1
- time_sig: 3/4
- max_poly: 3
- bar_density_mean: 8.25
- bar_density_p90: 10.0
- tracks: 2
- pitch_min: 52
- pitch_max: 100

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
- base_shift: -12
- octave_windows: w00-w02:-12
- lead_notes: 51
- lead_from_melody_track: 51 (100.0%)
- lead_from_top_note: 51 (100.0%)
- fallback_lead_notes: 0
- lead_midlead_moved: 39
- lead_midrow_notes: 47
- lead_highrow_notes: 3
- support_notes_pruned: 0
- chromatic_tokens: 43
