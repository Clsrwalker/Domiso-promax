# Analysis (Yihuan 36-Key MelodyLock Script): bach-toccata-and-fugue-in-d-minor-piano-solo.mid

## Metrics
- note_count: 4122
- duration_s: 439.1054577532607
- tempo0: 60
- tempo_events: 46
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 28.825174825174827
- bar_density_p90: 48.0
- tracks: 2
- pitch_min: 20
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
- base_shift: 2
- dynamic_windows: w00-w17:+1, w18-w20:+5, w21-w35:+3
- lead_notes: 1619
- lead_from_melody_track: 1522 (94.0%)
- lead_from_top_note: 1610 (99.4%)
- fallback_lead_notes: 97
- support_notes_pruned: 325
- chromatic_tokens: 1907
