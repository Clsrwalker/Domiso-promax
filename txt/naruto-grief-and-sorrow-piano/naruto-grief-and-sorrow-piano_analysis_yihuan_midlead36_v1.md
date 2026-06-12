# Analysis (Yihuan 36-Key MidLead36 Script): naruto-grief-and-sorrow-piano.mid

## Metrics
- note_count: 765
- duration_s: 208.78300437782562
- tempo0: 68
- tempo_events: 13
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 14.433962264150944
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 26
- pitch_max: 93

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
- octave_windows: w00-w13:+0
- lead_notes: 223
- lead_from_melody_track: 195 (87.4%)
- lead_from_top_note: 223 (100.0%)
- fallback_lead_notes: 28
- lead_midlead_moved: 81
- lead_midrow_notes: 190
- lead_highrow_notes: 9
- support_notes_pruned: 2
- chromatic_tokens: 33
