# Analysis (Sky MelodyLock Script): liang-zhi-lao-hu.mid

## Metrics
- note_count: 146
- duration_s: 17.5
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 16.22222222222222
- bar_density_p90: 21.0
- tracks: 4
- pitch_min: 48
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
- base_shift: 7
- dynamic_windows: w00-w02:+7
- lead_notes: 32
- lead_from_melody_track: 22 (68.8%)
- lead_from_top_note: 32 (100.0%)
- fallback_lead_notes: 10
- lead_speed_pruned: 0
- support_notes_pruned: 8
- input_budget_dropped: 2

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 250.0
- same_key_min_gap_ms: 250.0
