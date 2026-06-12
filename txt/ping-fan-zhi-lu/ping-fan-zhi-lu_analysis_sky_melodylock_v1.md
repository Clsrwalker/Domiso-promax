# Analysis (Sky MelodyLock Script): ping-fan-zhi-lu.mid

## Metrics
- note_count: 2011
- duration_s: 345.20547945205476
- tempo0: 73
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.33653846153846
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 33
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
- base_shift: 3
- dynamic_windows: w00-w25:+3
- lead_notes: 758
- lead_from_melody_track: 654 (86.3%)
- lead_from_top_note: 758 (100.0%)
- fallback_lead_notes: 104
- lead_speed_pruned: 0
- support_notes_pruned: 25
- input_budget_dropped: 80

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 205.5
- same_key_min_gap_ms: 205.5
