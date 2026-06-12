# Analysis (Yihuan 36-Key MelodyLock Script): sis-puella-magica-puella-magi-madoka-magica-yuki-kajiura.mid

## Metrics
- note_count: 1386
- duration_s: 189.5
- tempo0: 120
- tempo_events: 1
- time_sig: 3/4
- max_poly: 9
- bar_density_mean: 11.0
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 27
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
- base_shift: 1
- dynamic_windows: w00-w05:-1, w06-w12:+4, w13-w23:-1
- lead_notes: 414
- lead_from_melody_track: 392 (94.7%)
- lead_from_top_note: 414 (100.0%)
- fallback_lead_notes: 22
- support_notes_pruned: 0
- chromatic_tokens: 667
