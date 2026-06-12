# Analysis (Yihuan 36-Key MelodyLock Script): yan-yuan-xue-zhi-qian.mid

## Metrics
- note_count: 896
- duration_s: 132.2400442477876
- tempo0: 120
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.575757575757576
- bar_density_p90: 20.3
- tracks: 2
- pitch_min: 16
- pitch_max: 102

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
- dynamic_windows: w00-w04:-2, w05-w14:-7, w15-w16:-5
- lead_notes: 390
- lead_from_melody_track: 377 (96.7%)
- lead_from_top_note: 390 (100.0%)
- fallback_lead_notes: 13
- support_notes_pruned: 2
- chromatic_tokens: 474
