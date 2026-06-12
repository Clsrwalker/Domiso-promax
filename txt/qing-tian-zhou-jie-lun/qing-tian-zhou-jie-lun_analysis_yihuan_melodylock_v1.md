# Analysis (Yihuan 36-Key MelodyLock Script): qing-tian-zhou-jie-lun.mid

## Metrics
- note_count: 860
- duration_s: 222.3547794117647
- tempo0: 68
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 13.65079365079365
- bar_density_p90: 20.4
- tracks: 2
- pitch_min: 38
- pitch_max: 81

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
- base_shift: 2
- dynamic_windows: w00-w04:+5, w05-w15:+2
- lead_notes: 488
- lead_from_melody_track: 472 (96.7%)
- lead_from_top_note: 488 (100.0%)
- fallback_lead_notes: 16
- support_notes_pruned: 0
- chromatic_tokens: 183
