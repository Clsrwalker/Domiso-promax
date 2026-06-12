# Analysis (Yihuan 36-Key MelodyLock Script): believer.mid

## Metrics
- note_count: 2953
- duration_s: 220.5483870967742
- tempo0: 186
- tempo_events: 1
- time_sig: 12/8
- max_poly: 6
- bar_density_mean: 25.903508771929825
- bar_density_p90: 38.0
- tracks: 2
- pitch_min: 21
- pitch_max: 93

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
- dynamic_windows: w00-w02:+6, w03-w23:+9, w24-w42:+6
- lead_notes: 1077
- lead_from_melody_track: 866 (80.4%)
- lead_from_top_note: 1063 (98.7%)
- fallback_lead_notes: 211
- support_notes_pruned: 221
- chromatic_tokens: 1464
