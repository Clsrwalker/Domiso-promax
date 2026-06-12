# Analysis (Yihuan 36-Key MidLead36 Script): fan-wu-tuo-bang.mid

## Metrics
- note_count: 1140
- duration_s: 148.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.405405405405405
- bar_density_p90: 21.0
- tracks: 2
- pitch_min: 43
- pitch_max: 79

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
- octave_windows: w00-w18:+0
- lead_notes: 641
- lead_from_melody_track: 639 (99.7%)
- lead_from_top_note: 641 (100.0%)
- fallback_lead_notes: 2
- lead_midlead_moved: 219
- lead_midrow_notes: 442
- lead_highrow_notes: 4
- support_notes_pruned: 0
- chromatic_tokens: 40
