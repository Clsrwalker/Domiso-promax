# Analysis (Yihuan 36-Key MidLead36 Script): xia-shan.mid

## Metrics
- note_count: 1411
- duration_s: 169.609756097561
- tempo0: 82
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 24.32758620689655
- bar_density_p90: 31.0
- tracks: 2
- pitch_min: 32
- pitch_max: 90

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
- octave_windows: w00-w14:+0
- lead_notes: 532
- lead_from_melody_track: 531 (99.8%)
- lead_from_top_note: 532 (100.0%)
- fallback_lead_notes: 1
- lead_midlead_moved: 310
- lead_midrow_notes: 455
- lead_highrow_notes: 17
- support_notes_pruned: 176
- chromatic_tokens: 737
