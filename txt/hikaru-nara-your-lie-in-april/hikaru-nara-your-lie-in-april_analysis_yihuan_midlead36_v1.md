# Analysis (Yihuan 36-Key MidLead36 Script): hikaru-nara-your-lie-in-april.mid

## Metrics
- note_count: 1018
- duration_s: 92.92500000000001
- tempo0: 80
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 32.83870967741935
- bar_density_p90: 45.6
- tracks: 2
- pitch_min: 30
- pitch_max: 97

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
- octave_windows: w00-w07:+0
- lead_notes: 231
- lead_from_melody_track: 227 (98.3%)
- lead_from_top_note: 231 (100.0%)
- fallback_lead_notes: 4
- lead_midlead_moved: 143
- lead_midrow_notes: 180
- lead_highrow_notes: 4
- support_notes_pruned: 110
- chromatic_tokens: 317
