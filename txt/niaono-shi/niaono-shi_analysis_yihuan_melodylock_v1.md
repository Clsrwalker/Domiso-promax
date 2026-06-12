# Analysis (Yihuan 36-Key MelodyLock Script): niaono-shi.mid

## Metrics
- note_count: 3718
- duration_s: 374.7561475409836
- tempo0: 122
- tempo_events: 2
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 19.77659574468085
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 27
- pitch_max: 95

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
- base_shift: 5
- dynamic_windows: w00-w22:+5, w23-w28:+3, w29-w46:+5
- lead_notes: 1048
- lead_from_melody_track: 962 (91.8%)
- lead_from_top_note: 1038 (99.0%)
- fallback_lead_notes: 86
- support_notes_pruned: 188
- chromatic_tokens: 980
