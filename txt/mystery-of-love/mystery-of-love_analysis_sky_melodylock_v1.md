# Analysis (Sky MelodyLock Script): mystery-of-love.mid

## Metrics
- note_count: 1571
- duration_s: 201.85
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.71
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 47
- pitch_max: 88

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
- base_shift: 10
- dynamic_windows: w00-w20:+10, w21-w23:+12, w24-w24:+10
- lead_notes: 427
- lead_from_melody_track: 410 (96.0%)
- lead_from_top_note: 427 (100.0%)
- fallback_lead_notes: 17
- lead_speed_pruned: 0
- support_notes_pruned: 8
- input_budget_dropped: 4

## Input Stability
- clusters_per_sec_peak: 8.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
