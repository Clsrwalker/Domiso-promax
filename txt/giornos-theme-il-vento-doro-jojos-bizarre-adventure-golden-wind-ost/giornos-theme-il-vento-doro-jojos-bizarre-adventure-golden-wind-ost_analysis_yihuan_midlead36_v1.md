# Analysis (Yihuan 36-Key MidLead36 Script): giornos-theme-il-vento-doro-jojos-bizarre-adventure-golden-wind-ost.mid

## Metrics
- note_count: 2890
- duration_s: 289.46666666666664
- tempo0: 135
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 18.0625
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 30
- pitch_max: 98

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
- octave_windows: w00-w39:+0
- lead_notes: 968
- lead_from_melody_track: 882 (91.1%)
- lead_from_top_note: 966 (99.8%)
- fallback_lead_notes: 86
- lead_midlead_moved: 477
- lead_midrow_notes: 752
- lead_highrow_notes: 69
- support_notes_pruned: 87
- chromatic_tokens: 734
