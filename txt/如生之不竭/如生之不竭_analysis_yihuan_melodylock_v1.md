# Analysis (Yihuan 36-Key MelodyLock Script): 如生之不竭.mid

## Metrics
- note_count: 1562
- duration_s: 151.69811320754715
- tempo0: 106
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 23.313432835820894
- bar_density_p90: 33.4
- tracks: 2
- pitch_min: 38
- pitch_max: 95

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
- dynamic_windows: w00-w07:-5, w08-w09:-8, w10-w16:-2
- lead_notes: 699
- lead_from_melody_track: 667 (95.4%)
- lead_from_top_note: 699 (100.0%)
- fallback_lead_notes: 32
- support_notes_pruned: 27
- chromatic_tokens: 238
