# Analysis (Sky MelodyLock Script): centuries.mid

## Metrics
- note_count: 1519
- duration_s: 230.0
- tempo0: 90
- tempo_events: 1
- time_sig: 1/4
- max_poly: 8
- bar_density_mean: 4.454545454545454
- bar_density_p90: 8.0
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
- base_shift: 5
- dynamic_windows: w00-w21:+5
- lead_notes: 575
- lead_from_melody_track: 571 (99.3%)
- lead_from_top_note: 575 (100.0%)
- fallback_lead_notes: 4
- lead_speed_pruned: 0
- support_notes_pruned: 54
- input_budget_dropped: 90

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 166.7
- same_key_min_gap_ms: 166.7
