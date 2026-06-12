# Analysis (Yihuan 36-Key MidLead36 Script): 仙境的夜想.mid

## Metrics
- note_count: 522
- duration_s: 114.82931836057672
- tempo0: 137
- tempo_events: 9
- time_sig: 3/4
- max_poly: 6
- bar_density_mean: 6.0
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 34
- pitch_max: 97

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
- octave_windows: w00-w16:+0
- lead_notes: 232
- lead_from_melody_track: 189 (81.5%)
- lead_from_top_note: 232 (100.0%)
- fallback_lead_notes: 43
- lead_midlead_moved: 123
- lead_midrow_notes: 197
- lead_highrow_notes: 5
- support_notes_pruned: 29
- chromatic_tokens: 362
