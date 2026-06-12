# Analysis (Yihuan 36-Key MidLead36 Script): bach-toccata-and-fugue-in-d-minor-piano-solo.mid

## Metrics
- note_count: 4122
- duration_s: 439.1054577532607
- tempo0: 60
- tempo_events: 46
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 28.825174825174827
- bar_density_p90: 48.0
- tracks: 2
- pitch_min: 20
- pitch_max: 86

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
- octave_windows: w00-w35:+0
- lead_notes: 1619
- lead_from_melody_track: 1522 (94.0%)
- lead_from_top_note: 1601 (98.9%)
- fallback_lead_notes: 97
- lead_midlead_moved: 803
- lead_midrow_notes: 1446
- lead_highrow_notes: 72
- support_notes_pruned: 131
- chromatic_tokens: 756
