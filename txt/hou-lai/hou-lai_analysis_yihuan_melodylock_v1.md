# Analysis (Yihuan 36-Key MelodyLock Script): hou-lai.mid

## Metrics
- note_count: 1465
- duration_s: 316.8
- tempo0: 75
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 14.797979797979798
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 24
- pitch_max: 98

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
- base_shift: 3
- dynamic_windows: w00-w02:+1, w03-w09:+6, w10-w24:+1
- lead_notes: 567
- lead_from_melody_track: 542 (95.6%)
- lead_from_top_note: 567 (100.0%)
- fallback_lead_notes: 25
- support_notes_pruned: 3
- chromatic_tokens: 750
