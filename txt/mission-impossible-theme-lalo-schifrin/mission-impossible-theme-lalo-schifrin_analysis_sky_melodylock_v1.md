# Analysis (Sky MelodyLock Script): mission-impossible-theme-lalo-schifrin.mid

## Metrics
- note_count: 2756
- duration_s: 193.805
- tempo0: 100
- tempo_events: 3
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 25.51851851851852
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 26
- pitch_max: 108

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
- dynamic_windows: w00-w06:+9, w07-w20:+7
- lead_notes: 838
- lead_from_melody_track: 824 (98.3%)
- lead_from_top_note: 790 (94.3%)
- fallback_lead_notes: 14
- lead_speed_pruned: 0
- support_notes_pruned: 460
- input_budget_dropped: 45

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 150.0
- same_key_min_gap_ms: 150.0
