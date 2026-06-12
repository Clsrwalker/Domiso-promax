# Analysis (Yihuan 36-Key MidLead36 Script): 一颗方糖悬滞的时间.mid

## Metrics
- note_count: 959
- duration_s: 198.02102063878743
- tempo0: 100
- tempo_events: 11
- time_sig: 1/4
- max_poly: 5
- bar_density_mean: 2.9782608695652173
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 37
- pitch_max: 87

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
- octave_windows: w00-w20:+0
- lead_notes: 444
- lead_from_melody_track: 429 (96.6%)
- lead_from_top_note: 443 (99.8%)
- fallback_lead_notes: 15
- lead_midlead_moved: 255
- lead_midrow_notes: 382
- lead_highrow_notes: 24
- support_notes_pruned: 0
- chromatic_tokens: 747
