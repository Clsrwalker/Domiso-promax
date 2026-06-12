# Analysis (Yihuan 36-Key MidLead36 Script): renai-circulation-lian-aisakyureshon-full-score-for-piano.mid

## Metrics
- note_count: 2125
- duration_s: 251.475
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 16.865079365079364
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 25
- pitch_max: 92

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
- lead_notes: 851
- lead_from_melody_track: 725 (85.2%)
- lead_from_top_note: 834 (98.0%)
- fallback_lead_notes: 126
- lead_midlead_moved: 626
- lead_midrow_notes: 689
- lead_highrow_notes: 8
- support_notes_pruned: 163
- chromatic_tokens: 745
