# Analysis (Yihuan 36-Key MidLead36 Script): 「左道的胜义尊」.mid

## Metrics
- note_count: 2104
- duration_s: 296.36287313432837
- tempo0: 64
- tempo_events: 2
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 16.832
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 33
- pitch_max: 98

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
- octave_windows: w00-w31:+0
- lead_notes: 778
- lead_from_melody_track: 713 (91.6%)
- lead_from_top_note: 778 (100.0%)
- fallback_lead_notes: 65
- lead_midlead_moved: 484
- lead_midrow_notes: 680
- lead_highrow_notes: 29
- support_notes_pruned: 45
- chromatic_tokens: 701
