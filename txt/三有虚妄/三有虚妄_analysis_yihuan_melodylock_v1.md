# Analysis (Yihuan 36-Key MelodyLock Script): 三有虚妄.mid

## Metrics
- note_count: 376
- duration_s: 91.89526936174494
- tempo0: 65
- tempo_events: 5
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 11.75
- bar_density_p90: 18.7
- tracks: 2
- pitch_min: 40
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
- dynamic_windows: w00-w05:+5
- lead_notes: 138
- lead_from_melody_track: 134 (97.1%)
- lead_from_top_note: 138 (100.0%)
- fallback_lead_notes: 4
- support_notes_pruned: 2
- chromatic_tokens: 129
