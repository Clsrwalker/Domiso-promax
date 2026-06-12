# Analysis (Yihuan 36-Key MelodyLock Script): attack-on-titan-call-of-silence-piano.mid

## Metrics
- note_count: 689
- duration_s: 137.00104166666668
- tempo0: 120
- tempo_events: 1
- time_sig: 2/4
- max_poly: 8
- bar_density_mean: 5.0661764705882355
- bar_density_p90: 10.0
- tracks: 2
- pitch_min: 25
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
- base_shift: 10
- dynamic_windows: w00-w05:+7, w06-w14:+10, w15-w16:+7
- lead_notes: 199
- lead_from_melody_track: 145 (72.9%)
- lead_from_top_note: 197 (99.0%)
- fallback_lead_notes: 54
- support_notes_pruned: 14
- chromatic_tokens: 224
