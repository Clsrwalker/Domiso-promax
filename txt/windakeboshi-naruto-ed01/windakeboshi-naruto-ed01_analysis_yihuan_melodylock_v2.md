# Analysis (Yihuan 36-Key MelodyLock Script): windakeboshi-naruto-ed01.mid

## Metrics
- note_count: 1647
- duration_s: 195.9715909090909
- tempo0: 88
- tempo_events: 1
- time_sig: 5/8
- max_poly: 6
- bar_density_mean: 14.321739130434782
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 36
- pitch_max: 86

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
- base_shift: 4
- dynamic_windows: w00-w00:+1, w01-w16:+4, w17-w17:+7
- lead_notes: 468
- lead_from_melody_track: 462 (98.7%)
- lead_from_top_note: 468 (100.0%)
- fallback_lead_notes: 6
- support_notes_pruned: 15
- chromatic_tokens: 195
