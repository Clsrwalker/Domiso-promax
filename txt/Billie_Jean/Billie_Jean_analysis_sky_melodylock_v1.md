# Analysis (Sky MelodyLock Script): Billie_Jean.mid

## Metrics
- note_count: 5972
- duration_s: 294.91525423728814
- tempo0: 118
- tempo_events: 1
- time_sig: 4/4
- max_poly: 13
- bar_density_mean: 41.186206896551724
- bar_density_p90: 50.0
- tracks: 9
- pitch_min: 30
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
- base_shift: -11
- dynamic_windows: w00-w36:-11
- lead_notes: 1156
- lead_from_melody_track: 1140 (98.6%)
- lead_from_top_note: 1152 (99.7%)
- fallback_lead_notes: 16
- lead_speed_pruned: 0
- support_notes_pruned: 1238
- input_budget_dropped: 0

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 127.1
- same_key_min_gap_ms: 127.1
