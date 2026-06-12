# Analysis (Yihuan 36-Key MidLead36 Script): dzwony-na-nieszpory-hoyo-mix.mid

## Metrics
- note_count: 722
- duration_s: 98.06650901373021
- tempo0: 120
- tempo_events: 4
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 11.107692307692307
- bar_density_p90: 19.0
- tracks: 4
- pitch_min: 36
- pitch_max: 88

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
- octave_windows: w00-w12:+0
- lead_notes: 225
- lead_from_melody_track: 105 (46.7%)
- lead_from_top_note: 208 (92.4%)
- fallback_lead_notes: 120
- lead_midlead_moved: 151
- lead_midrow_notes: 209
- lead_highrow_notes: 3
- support_notes_pruned: 61
- chromatic_tokens: 10
