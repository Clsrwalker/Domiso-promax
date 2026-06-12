# Analysis (Yihuan 36-Key MelodyLock Script): alan-walker-darkside-piano.mid

## Metrics
- note_count: 1341
- duration_s: 217.34117647058824
- tempo0: 170
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 8.707792207792208
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 36
- pitch_max: 84

## Recommended Profile
- yihuan_melodylock
- reason: default Yihuan 36-key melodylock profile

## Yihuan 36-Key MelodyLock Intent
- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- avoid turning sustained melody into stacked lead chords
- keep support notes in B/C instead of letting A absorb the whole piano texture
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 11
- dynamic_windows: w00-w25:+11, w26-w38:+9
- lead_notes: 442
- lead_from_melody_track: 416 (94.1%)
- lead_from_top_note: 442 (100.0%)
- fallback_lead_notes: 26
- support_notes_pruned: 15
- chromatic_tokens: 938
