# Analysis (Yihuan 36-Key MelodyLock Script): scaramouche-boss-theme-genshin-impact-32-yu-peng-chen.mid

## Metrics
- note_count: 1996
- duration_s: 194.984375
- tempo0: 160
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 15.353846153846154
- bar_density_p90: 23.0
- tracks: 2
- pitch_min: 25
- pitch_max: 97

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
- base_shift: 1
- dynamic_windows: w00-w15:+1, w16-w23:-2, w24-w32:+4
- lead_notes: 557
- lead_from_melody_track: 527 (94.6%)
- lead_from_top_note: 552 (99.1%)
- fallback_lead_notes: 30
- support_notes_pruned: 93
- chromatic_tokens: 947
