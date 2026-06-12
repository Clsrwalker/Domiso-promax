# Analysis (Sky MelodyLock Script): ce-lian.mid

## Metrics
- note_count: 1312
- duration_s: 206.76923076923077
- tempo0: 65
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.428571428571427
- bar_density_p90: 41.0
- tracks: 2
- pitch_min: 34
- pitch_max: 84

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
- dynamic_windows: w00-w13:+7
- lead_notes: 450
- lead_from_melody_track: 381 (84.7%)
- lead_from_top_note: 450 (100.0%)
- fallback_lead_notes: 69
- lead_speed_pruned: 0
- support_notes_pruned: 0
- input_budget_dropped: 0

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 230.8
- same_key_min_gap_ms: 230.8
