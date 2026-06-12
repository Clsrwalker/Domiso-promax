# Analysis (Sky MelodyLock Script): shock-tv-ver.mid

## Metrics
- note_count: 329
- duration_s: 83.48007246376811
- tempo0: 69
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.708333333333334
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 40
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
- base_shift: 1
- dynamic_windows: w00-w05:+1
- lead_notes: 137
- lead_from_melody_track: 134 (97.8%)
- lead_from_top_note: 137 (100.0%)
- fallback_lead_notes: 3
- lead_speed_pruned: 0
- support_notes_pruned: 4
- input_budget_dropped: 12

## Input Stability
- clusters_per_sec_peak: 4.0
- min_cluster_gap_ms: 217.4
- same_key_min_gap_ms: 217.4
