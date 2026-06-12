# Analysis (Yihuan 36-Key MelodyLock Script): kokoronashi-xin-zuoshi.mid

## Metrics
- note_count: 1978
- duration_s: 395.4170256079848
- tempo0: 76
- tempo_events: 35
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 21.268817204301076
- bar_density_p90: 35.0
- tracks: 2
- pitch_min: 26
- pitch_max: 93

## Recommended Profile
- yihuan_melodylock_dense
- reason: dense piano texture -> yihuan_melodylock_dense

## Yihuan 36-Key MelodyLock Intent
- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- avoid turning sustained melody into stacked lead chords
- keep support notes in B/C instead of letting A absorb the whole piano texture
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: -5
- dynamic_windows: w00-w05:-2, w06-w19:-5, w20-w23:-2
- lead_notes: 858
- lead_from_melody_track: 735 (85.7%)
- lead_from_top_note: 853 (99.4%)
- fallback_lead_notes: 123
- support_notes_pruned: 50
- chromatic_tokens: 364
