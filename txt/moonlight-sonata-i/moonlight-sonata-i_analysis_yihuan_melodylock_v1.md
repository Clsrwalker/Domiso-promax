# Analysis (Yihuan 36-Key MelodyLock Script): moonlight-sonata-i.mid

## Metrics
- note_count: 1164
- duration_s: 368.0027777777778
- tempo0: 45
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 16.869565217391305
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 29
- pitch_max: 87

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
- dynamic_windows: w00-w06:+8, w07-w08:+4, w09-w17:+7
- lead_notes: 807
- lead_from_melody_track: 802 (99.4%)
- lead_from_top_note: 807 (100.0%)
- fallback_lead_notes: 5
- support_notes_pruned: 28
- chromatic_tokens: 517
