# Analysis (Sky MelodyLock Script): aizo-king-gnu.mid

## Metrics
- note_count: 1237
- duration_s: 86.84210526315789
- tempo0: 190
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.92753623188406
- bar_density_p90: 25.0
- tracks: 2
- pitch_min: 33
- pitch_max: 100

## Recommended Profile
- sky_melodylock_dense
- reason: 15-key range + dense source -> sky_melodylock_dense

## Sky MelodyLock Intent
- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line
- force output into Sky's 15-key C4-C6 layout
- keep the hook away from the lowest row when a better transpose exists
- keep support notes in B/C instead of letting A absorb the whole piano texture
- target layout: Y U I O P / H J K L ; / N M , . /

## Extraction Summary
- base_shift: 12
- dynamic_windows: w00-w17:+12
- lead_notes: 465
- lead_from_melody_track: 444 (95.5%)
- lead_from_top_note: 459 (98.7%)
- fallback_lead_notes: 21
- lead_speed_pruned: 53
- support_notes_pruned: 157
- input_budget_dropped: 48

## Input Stability
- clusters_per_sec_peak: 9.0
- min_cluster_gap_ms: 78.9
- same_key_min_gap_ms: 157.9
