# Analysis (Sky MelodyLock Script): jue-bie-shu.mid

## Metrics
- note_count: 1607
- duration_s: 249.2121212121212
- tempo0: 90
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 14.87962962962963
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 26
- pitch_max: 98

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
- dynamic_windows: w00-w26:+7
- lead_notes: 571
- lead_from_melody_track: 570 (99.8%)
- lead_from_top_note: 571 (100.0%)
- fallback_lead_notes: 1
- lead_speed_pruned: 0
- support_notes_pruned: 68
- input_budget_dropped: 25

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 136.4
- same_key_min_gap_ms: 166.7
