# Analysis (Yihuan 36-Key MelodyLock Script): fur-elise-beethoven.mid

## Metrics
- note_count: 1040
- duration_s: 156.83901515151518
- tempo0: 72
- tempo_events: 2
- time_sig: 1/8
- max_poly: 6
- bar_density_mean: 2.7807486631016043
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 33
- pitch_max: 100

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
- base_shift: 4
- dynamic_windows: w00-w05:+4, w06-w11:+6
- lead_notes: 533
- lead_from_melody_track: 502 (94.2%)
- lead_from_top_note: 533 (100.0%)
- fallback_lead_notes: 31
- support_notes_pruned: 292
- chromatic_tokens: 467
