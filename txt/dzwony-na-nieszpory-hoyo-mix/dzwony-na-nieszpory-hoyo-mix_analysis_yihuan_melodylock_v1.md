# Analysis (Yihuan 36-Key MelodyLock Script): dzwony-na-nieszpory-hoyo-mix.mid

## Metrics
- note_count: 722
- duration_s: 98.06650901373021
- tempo0: 120
- tempo_events: 4
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 11.107692307692307
- bar_density_p90: 19.0
- tracks: 4
- pitch_min: 36
- pitch_max: 88

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
- base_shift: -5
- dynamic_windows: w00-w00:-2, w01-w12:-5
- lead_notes: 251
- lead_from_melody_track: 105 (41.8%)
- lead_from_top_note: 238 (94.8%)
- fallback_lead_notes: 146
- support_notes_pruned: 13
- chromatic_tokens: 83
