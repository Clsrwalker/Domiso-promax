# Analysis (Sky MelodyLock Script): yoasobi-tabun-tabunprobably.mid

## Metrics
- note_count: 1836
- duration_s: 257.5
- tempo0: 90
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 18.927835051546392
- bar_density_p90: 26.2
- tracks: 2
- pitch_min: 42
- pitch_max: 94

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
- dynamic_windows: w00-w16:+7, w17-w24:+6
- lead_notes: 663
- lead_from_melody_track: 620 (93.5%)
- lead_from_top_note: 655 (98.8%)
- fallback_lead_notes: 43
- lead_speed_pruned: 0
- support_notes_pruned: 137
- input_budget_dropped: 2

## Input Stability
- clusters_per_sec_peak: 4.0
- min_cluster_gap_ms: 166.7
- same_key_min_gap_ms: 166.7
