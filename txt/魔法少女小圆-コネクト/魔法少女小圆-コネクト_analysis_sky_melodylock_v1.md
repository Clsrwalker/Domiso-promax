# Analysis (Sky MelodyLock Script): 魔法少女小圆 - コネクト.mid

## Metrics
- note_count: 1041
- duration_s: 88.0
- tempo0: 180
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 15.772727272727273
- bar_density_p90: 22.0
- tracks: 1
- pitch_min: 45
- pitch_max: 81

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
- dynamic_windows: w00-w16:+12
- lead_notes: 397
- lead_from_melody_track: 397 (100.0%)
- lead_from_top_note: 386 (97.2%)
- fallback_lead_notes: 0
- lead_speed_pruned: 2
- support_notes_pruned: 0
- input_budget_dropped: 36

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 83.3
- same_key_min_gap_ms: 166.7
