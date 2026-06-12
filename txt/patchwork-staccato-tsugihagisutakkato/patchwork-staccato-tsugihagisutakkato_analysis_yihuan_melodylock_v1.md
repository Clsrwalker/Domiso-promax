# Analysis (Yihuan 36-Key MelodyLock Script): patchwork-staccato-tsugihagisutakkato.mid

## Metrics
- note_count: 2847
- duration_s: 242.36330935251797
- tempo0: 139
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 20.19148936170213
- bar_density_p90: 29.8
- tracks: 2
- pitch_min: 36
- pitch_max: 101

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
- dynamic_windows: w00-w14:-5, w15-w15:-8, w16-w35:-5
- lead_notes: 1046
- lead_from_melody_track: 962 (92.0%)
- lead_from_top_note: 1042 (99.6%)
- fallback_lead_notes: 84
- support_notes_pruned: 73
- chromatic_tokens: 378
