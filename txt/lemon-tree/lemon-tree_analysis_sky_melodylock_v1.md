# Analysis (Sky MelodyLock Script): lemon-tree.mid

## Metrics
- note_count: 1471
- duration_s: 193.62857142857143
- tempo0: 140
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 13.017699115044248
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 43
- pitch_max: 77

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
- base_shift: 7
- dynamic_windows: w00-w28:+7
- lead_notes: 503
- lead_from_melody_track: 424 (84.3%)
- lead_from_top_note: 503 (100.0%)
- fallback_lead_notes: 79
- lead_speed_pruned: 0
- support_notes_pruned: 0
- input_budget_dropped: 3

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 107.1
- same_key_min_gap_ms: 214.3
