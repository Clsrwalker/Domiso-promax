# Analysis (Yihuan 36-Key MelodyLock Script): mystery-of-love.mid

## Metrics
- note_count: 1571
- duration_s: 201.85
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.71
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 47
- pitch_max: 88

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
- base_shift: -3
- dynamic_windows: w00-w15:+0, w16-w22:-5, w23-w24:+0
- lead_notes: 427
- lead_from_melody_track: 410 (96.0%)
- lead_from_top_note: 427 (100.0%)
- fallback_lead_notes: 17
- support_notes_pruned: 0
- chromatic_tokens: 290
