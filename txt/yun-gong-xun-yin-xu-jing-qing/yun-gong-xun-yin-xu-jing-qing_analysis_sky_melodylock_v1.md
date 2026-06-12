# Analysis (Sky MelodyLock Script): yun-gong-xun-yin-xu-jing-qing.mid

## Metrics
- note_count: 1542
- duration_s: 145.7142857142857
- tempo0: 140
- tempo_events: 1
- time_sig: 4/4
- max_poly: 10
- bar_density_mean: 18.357142857142858
- bar_density_p90: 23.0
- tracks: 3
- pitch_min: 40
- pitch_max: 90

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
- base_shift: 5
- dynamic_windows: w00-w03:+7, w04-w11:+5, w12-w20:+3
- lead_notes: 252
- lead_from_melody_track: 212 (84.1%)
- lead_from_top_note: 234 (92.9%)
- fallback_lead_notes: 40
- lead_speed_pruned: 0
- support_notes_pruned: 287
- input_budget_dropped: 6

## Input Stability
- clusters_per_sec_peak: 9.0
- min_cluster_gap_ms: 107.1
- same_key_min_gap_ms: 107.1
