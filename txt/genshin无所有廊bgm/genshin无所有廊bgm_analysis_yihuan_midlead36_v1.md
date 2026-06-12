# Analysis (Yihuan 36-Key MidLead36 Script): genshin无所有廊bgm.mid

## Metrics
- note_count: 886
- duration_s: 183.3556818181818
- tempo0: 110
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 11.35897435897436
- bar_density_p90: 16.1
- tracks: 2
- pitch_min: 42
- pitch_max: 92

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
- octave_windows: w00-w19:+0
- lead_notes: 470
- lead_from_melody_track: 410 (87.2%)
- lead_from_top_note: 470 (100.0%)
- fallback_lead_notes: 60
- lead_midlead_moved: 289
- lead_midrow_notes: 434
- lead_highrow_notes: 21
- support_notes_pruned: 15
- chromatic_tokens: 764
