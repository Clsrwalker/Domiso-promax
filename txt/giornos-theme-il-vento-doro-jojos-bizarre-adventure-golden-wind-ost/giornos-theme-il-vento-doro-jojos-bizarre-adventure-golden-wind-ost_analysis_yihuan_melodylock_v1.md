# Analysis (Yihuan 36-Key MelodyLock Script): giornos-theme-il-vento-doro-jojos-bizarre-adventure-golden-wind-ost.mid

## Metrics
- note_count: 2890
- duration_s: 289.46666666666664
- tempo0: 135
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 18.0625
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 30
- pitch_max: 98

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
- dynamic_windows: w00-w02:+8, w03-w31:+5, w32-w39:+4
- lead_notes: 968
- lead_from_melody_track: 882 (91.1%)
- lead_from_top_note: 966 (99.8%)
- fallback_lead_notes: 86
- support_notes_pruned: 61
- chromatic_tokens: 749
