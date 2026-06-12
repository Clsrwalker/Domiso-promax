# Analysis (Sky MelodyLock Script): nod-krai.mid

## Metrics
- note_count: 2539
- duration_s: 254.90157128257536
- tempo0: 76
- tempo_events: 2
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 24.650485436893202
- bar_density_p90: 38.0
- tracks: 2
- pitch_min: 21
- pitch_max: 99

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
- base_shift: 9
- dynamic_windows: w00-w20:+9, w21-w25:+7
- lead_notes: 713
- lead_from_melody_track: 707 (99.2%)
- lead_from_top_note: 699 (98.0%)
- fallback_lead_notes: 6
- lead_speed_pruned: 0
- support_notes_pruned: 371
- input_budget_dropped: 60

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 145.6
- same_key_min_gap_ms: 145.6
