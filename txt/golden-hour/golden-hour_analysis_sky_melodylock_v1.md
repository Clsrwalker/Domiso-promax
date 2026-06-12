# Analysis (Sky MelodyLock Script): golden-hour.mid

## Metrics
- note_count: 1073
- duration_s: 90.0
- tempo0: 96
- tempo_events: 1
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 44.708333333333336
- bar_density_p90: 59.0
- tracks: 2
- pitch_min: 40
- pitch_max: 92

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
- base_shift: 8
- dynamic_windows: w00-w08:+8
- lead_notes: 447
- lead_from_melody_track: 447 (100.0%)
- lead_from_top_note: 446 (99.8%)
- fallback_lead_notes: 0
- lead_speed_pruned: 0
- support_notes_pruned: 182
- input_budget_dropped: 23

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 156.2
- same_key_min_gap_ms: 156.2
