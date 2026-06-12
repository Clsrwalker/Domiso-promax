# Analysis (Sky MelodyLock Script): 起风了 C调.mid

## Metrics
- note_count: 1083
- duration_s: 204.0
- tempo0: 80
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 16.16417910447761
- bar_density_p90: 20.2
- tracks: 2
- pitch_min: 38
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
- lead_notes: 526
- lead_from_melody_track: 526 (100.0%)
- lead_from_top_note: 524 (99.6%)
- fallback_lead_notes: 0
- lead_speed_pruned: 0
- support_notes_pruned: 33
- input_budget_dropped: 4

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 187.5
- same_key_min_gap_ms: 187.5
