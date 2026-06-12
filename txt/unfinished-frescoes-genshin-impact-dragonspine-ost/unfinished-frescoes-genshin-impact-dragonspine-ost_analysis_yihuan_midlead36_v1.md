# Analysis (Yihuan 36-Key MidLead36 Script): unfinished-frescoes-genshin-impact-dragonspine-ost.mid

## Metrics
- note_count: 285
- duration_s: 83.52272727272727
- tempo0: 66
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 12.391304347826088
- bar_density_p90: 17.6
- tracks: 3
- pitch_min: 39
- pitch_max: 94

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
- base_shift: -12
- octave_windows: w00-w05:-12
- lead_notes: 144
- lead_from_melody_track: 78 (54.2%)
- lead_from_top_note: 142 (98.6%)
- fallback_lead_notes: 66
- lead_midlead_moved: 80
- lead_midrow_notes: 124
- lead_highrow_notes: 0
- support_notes_pruned: 13
- chromatic_tokens: 63
