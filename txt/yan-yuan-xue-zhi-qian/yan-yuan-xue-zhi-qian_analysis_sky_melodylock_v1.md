# Analysis (Sky MelodyLock Script): yan-yuan-xue-zhi-qian.mid

## Metrics
- note_count: 896
- duration_s: 132.2400442477876
- tempo0: 120
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.575757575757576
- bar_density_p90: 20.3
- tracks: 2
- pitch_min: 16
- pitch_max: 102

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
- base_shift: 1
- dynamic_windows: w00-w16:+1
- lead_notes: 390
- lead_from_melody_track: 377 (96.7%)
- lead_from_top_note: 390 (100.0%)
- fallback_lead_notes: 13
- lead_speed_pruned: 0
- support_notes_pruned: 102
- input_budget_dropped: 15

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
