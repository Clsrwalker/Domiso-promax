# Analysis (Yihuan 36-Key MelodyLock Script): chen-yi-xun-eason-chan-gu-yong-zhe.mid

## Metrics
- note_count: 1745
- duration_s: 254.97656250000003
- tempo0: 64
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 25.66176470588235
- bar_density_p90: 41.2
- tracks: 2
- pitch_min: 25
- pitch_max: 94

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
- base_shift: 8
- dynamic_windows: w00-w02:+8, w03-w04:+5, w05-w16:+8
- lead_notes: 592
- lead_from_melody_track: 589 (99.5%)
- lead_from_top_note: 592 (100.0%)
- fallback_lead_notes: 3
- support_notes_pruned: 115
- chromatic_tokens: 224
