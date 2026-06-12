# Analysis (Yihuan 36-Key MelodyLock Script): 起风了 C调.mid

## Metrics
- note_count: 1083
- duration_s: 204.0
- tempo0: 80
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 16.16417910447761
- bar_density_p90: 20.2
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
- base_shift: 7
- dynamic_windows: w00-w00:+10, w01-w05:+7, w06-w16:+4
- lead_notes: 526
- lead_from_melody_track: 526 (100.0%)
- lead_from_top_note: 526 (100.0%)
- fallback_lead_notes: 0
- support_notes_pruned: 4
- chromatic_tokens: 429
