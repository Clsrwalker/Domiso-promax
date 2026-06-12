# Analysis (Yihuan 36-Key MelodyLock Script): shi-nian-chen-yi-xun.mid

## Metrics
- note_count: 1751
- duration_s: 199.35483870967744
- tempo0: 124
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.166666666666668
- bar_density_p90: 25.7
- tracks: 2
- pitch_min: 27
- pitch_max: 89

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
- dynamic_windows: w00-w11:+7, w12-w20:+1, w21-w25:+7
- lead_notes: 493
- lead_from_melody_track: 448 (90.9%)
- lead_from_top_note: 493 (100.0%)
- fallback_lead_notes: 45
- support_notes_pruned: 34
- chromatic_tokens: 706
