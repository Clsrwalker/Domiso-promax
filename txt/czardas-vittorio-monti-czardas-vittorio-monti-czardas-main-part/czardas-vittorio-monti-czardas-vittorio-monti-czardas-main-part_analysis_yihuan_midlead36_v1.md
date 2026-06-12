# Analysis (Yihuan 36-Key MidLead36 Script): czardas-vittorio-monti-czardas-vittorio-monti-czardas-main-part.mid

## Metrics
- note_count: 902
- duration_s: 47.44186046511628
- tempo0: 172
- tempo_events: 1
- time_sig: 2/4
- max_poly: 4
- bar_density_mean: 13.264705882352942
- bar_density_p90: 17.0
- tracks: 2
- pitch_min: 41
- pitch_max: 86

## Recommended Profile
- yihuan_midlead36
- reason: default Yihuan 36-key midlead36 profile

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
- octave_windows: w00-w08:+0
- lead_notes: 402
- lead_from_melody_track: 366 (91.0%)
- lead_from_top_note: 402 (100.0%)
- fallback_lead_notes: 36
- lead_midlead_moved: 309
- lead_midrow_notes: 365
- lead_highrow_notes: 26
- support_notes_pruned: 2
- chromatic_tokens: 98
