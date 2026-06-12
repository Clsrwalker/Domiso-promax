# Analysis (Yihuan 36-Key MidLead36 Script): her-legacy-inazuma-world-bgm-genshin-impact.mid

## Metrics
- note_count: 296
- duration_s: 63.0015625
- tempo0: 80
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 14.095238095238095
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 35
- pitch_max: 83

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
- octave_windows: w00-w05:+0
- lead_notes: 115
- lead_from_melody_track: 79 (68.7%)
- lead_from_top_note: 115 (100.0%)
- fallback_lead_notes: 36
- lead_midlead_moved: 67
- lead_midrow_notes: 104
- lead_highrow_notes: 2
- support_notes_pruned: 27
- chromatic_tokens: 130
