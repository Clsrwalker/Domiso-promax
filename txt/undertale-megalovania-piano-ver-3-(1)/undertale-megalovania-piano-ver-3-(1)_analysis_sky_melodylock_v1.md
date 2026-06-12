# Analysis (Sky MelodyLock Script): undertale-megalovania-piano-ver-3 (1).mid

## Metrics
- note_count: 1816
- duration_s: 155.99375
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.28205128205128
- bar_density_p90: 40.0
- tracks: 2
- pitch_min: 34
- pitch_max: 93

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
- base_shift: 9
- dynamic_windows: w00-w04:+9, w05-w05:+7, w06-w19:+9
- lead_notes: 554
- lead_from_melody_track: 469 (84.7%)
- lead_from_top_note: 554 (100.0%)
- fallback_lead_notes: 85
- lead_speed_pruned: 0
- support_notes_pruned: 108
- input_budget_dropped: 85

## Input Stability
- clusters_per_sec_peak: 9.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
