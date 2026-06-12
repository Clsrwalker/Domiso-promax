# Analysis (Sky MelodyLock Script): passacaglia-johan-halvorsen.mid

## Metrics
- note_count: 1030
- duration_s: 136.52307692307693
- tempo0: 130
- tempo_events: 1
- time_sig: 4/4
- max_poly: 3
- bar_density_mean: 13.91891891891892
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 36
- pitch_max: 96

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
- dynamic_windows: w00-w18:+12
- lead_notes: 504
- lead_from_melody_track: 486 (96.4%)
- lead_from_top_note: 504 (100.0%)
- fallback_lead_notes: 18
- lead_speed_pruned: 0
- support_notes_pruned: 0
- input_budget_dropped: 24

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 230.8
- same_key_min_gap_ms: 461.5
