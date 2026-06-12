# Analysis (Yihuan 36-Key MidLead36 Script): shi-nian-chen-yi-xun.mid

## Metrics
- note_count: 1751
- duration_s: 199.35483870967744
- tempo0: 124
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.166666666666668
- bar_density_p90: 25.7
- tracks: 2
- pitch_min: 27
- pitch_max: 89

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
- octave_windows: w00-w25:+0
- lead_notes: 493
- lead_from_melody_track: 448 (90.9%)
- lead_from_top_note: 493 (100.0%)
- fallback_lead_notes: 45
- lead_midlead_moved: 182
- lead_midrow_notes: 401
- lead_highrow_notes: 45
- support_notes_pruned: 48
- chromatic_tokens: 962
