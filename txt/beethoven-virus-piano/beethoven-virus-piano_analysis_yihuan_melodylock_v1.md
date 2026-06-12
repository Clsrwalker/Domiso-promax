# Analysis (Yihuan 36-Key MelodyLock Script): beethoven-virus-piano.mid

## Metrics
- note_count: 2671
- duration_s: 216.73125
- tempo0: 160
- tempo_events: 3
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.07857142857143
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 21
- pitch_max: 100

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
- dynamic_windows: w00-w16:+6, w17-w28:+1, w29-w34:+3
- lead_notes: 1069
- lead_from_melody_track: 1012 (94.7%)
- lead_from_top_note: 1064 (99.5%)
- fallback_lead_notes: 57
- support_notes_pruned: 97
- chromatic_tokens: 1313
