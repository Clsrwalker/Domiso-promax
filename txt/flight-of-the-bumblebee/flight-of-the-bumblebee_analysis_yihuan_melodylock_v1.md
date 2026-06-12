# Analysis (Yihuan 36-Key MelodyLock Script): flight-of-the-bumblebee.mid

## Metrics
- note_count: 1882
- duration_s: 127.0625
- tempo0: 144
- tempo_events: 1
- time_sig: 2/4
- max_poly: 7
- bar_density_mean: 12.300653594771243
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 34
- pitch_max: 105

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
- base_shift: -2
- dynamic_windows: w00-w00:-5, w01-w13:+0, w14-w19:-5
- lead_notes: 1180
- lead_from_melody_track: 1175 (99.6%)
- lead_from_top_note: 1155 (97.9%)
- fallback_lead_notes: 5
- support_notes_pruned: 86
- chromatic_tokens: 637
