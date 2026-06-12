# Analysis (Yihuan 36-Key MidLead36 Script): fantaisie-impromptu-in-c-minor-chopin.mid

## Metrics
- note_count: 3049
- duration_s: 327.51022460328124
- tempo0: 168
- tempo_events: 38
- time_sig: 2/2
- max_poly: 6
- bar_density_mean: 22.094202898550726
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 100

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
- octave_windows: w00-w34:+0
- lead_notes: 1663
- lead_from_melody_track: 1605 (96.5%)
- lead_from_top_note: 1663 (100.0%)
- fallback_lead_notes: 58
- lead_midlead_moved: 979
- lead_midrow_notes: 1571
- lead_highrow_notes: 40
- support_notes_pruned: 186
- chromatic_tokens: 1838
