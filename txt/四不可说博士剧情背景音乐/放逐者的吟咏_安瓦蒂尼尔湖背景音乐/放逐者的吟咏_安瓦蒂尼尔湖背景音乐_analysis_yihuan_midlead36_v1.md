# Analysis (Yihuan 36-Key MidLead36 Script): 放逐者的吟咏_安瓦蒂尼尔湖背景音乐.mid

## Metrics
- note_count: 283
- duration_s: 125.0283203125
- tempo0: 128
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 4.287878787878788
- bar_density_p90: 7.0
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
- octave_windows: w00-w16:+0
- lead_notes: 173
- lead_from_melody_track: 148 (85.5%)
- lead_from_top_note: 173 (100.0%)
- fallback_lead_notes: 25
- lead_midlead_moved: 66
- lead_midrow_notes: 161
- lead_highrow_notes: 5
- support_notes_pruned: 8
- chromatic_tokens: 79
