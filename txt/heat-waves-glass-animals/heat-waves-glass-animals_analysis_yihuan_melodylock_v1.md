# Analysis (Yihuan 36-Key MelodyLock Script): heat-waves-glass-animals.mid

## Metrics
- note_count: 1593
- duration_s: 219.08333333333331
- tempo0: 81
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 21.82191780821918
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 28
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
- base_shift: 12
- dynamic_windows: w00-w00:+9, w01-w10:+12, w11-w18:+10
- lead_notes: 652
- lead_from_melody_track: 595 (91.3%)
- lead_from_top_note: 652 (100.0%)
- fallback_lead_notes: 57
- support_notes_pruned: 129
- chromatic_tokens: 570
