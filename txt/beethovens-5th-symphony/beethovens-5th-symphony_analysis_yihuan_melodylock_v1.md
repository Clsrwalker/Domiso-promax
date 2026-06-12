# Analysis (Yihuan 36-Key MelodyLock Script): beethovens-5th-symphony.mid

## Metrics
- note_count: 2834
- duration_s: 151.76999999999998
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 44.28125
- bar_density_p90: 122.5
- tracks: 2
- pitch_min: 26
- pitch_max: 91

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
- dynamic_windows: w00-w10:+4, w11-w13:+5, w14-w15:+2
- lead_notes: 688
- lead_from_melody_track: 668 (97.1%)
- lead_from_top_note: 688 (100.0%)
- fallback_lead_notes: 20
- support_notes_pruned: 576
- chromatic_tokens: 300
