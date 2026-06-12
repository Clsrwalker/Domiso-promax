# Analysis (Yihuan 36-Key MidLead36 Script): flower-dance-dj-okawari.mid

## Metrics
- note_count: 2332
- duration_s: 270.0657871540225
- tempo0: 80
- tempo_events: 12
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 22.20952380952381
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 31
- pitch_max: 104

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
- octave_windows: w00-w26:+0
- lead_notes: 1239
- lead_from_melody_track: 1233 (99.5%)
- lead_from_top_note: 1225 (98.9%)
- fallback_lead_notes: 6
- lead_midlead_moved: 758
- lead_midrow_notes: 1150
- lead_highrow_notes: 22
- support_notes_pruned: 2
- chromatic_tokens: 1647
