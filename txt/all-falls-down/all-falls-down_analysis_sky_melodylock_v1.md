# Analysis (Sky MelodyLock Script): all-falls-down.mid

## Metrics
- note_count: 1618
- duration_s: 194.66326530612244
- tempo0: 98
- tempo_events: 1
- time_sig: 1/4
- max_poly: 7
- bar_density_mean: 5.088050314465409
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 42
- pitch_max: 85

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
- base_shift: 11
- dynamic_windows: w00-w19:+11
- lead_notes: 503
- lead_from_melody_track: 473 (94.0%)
- lead_from_top_note: 503 (100.0%)
- fallback_lead_notes: 30
- lead_speed_pruned: 0
- support_notes_pruned: 53
- input_budget_dropped: 68

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 153.1
- same_key_min_gap_ms: 153.1
