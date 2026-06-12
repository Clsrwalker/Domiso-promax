# Analysis (Sky MelodyLock Script): 三有虚妄.mid

## Metrics
- note_count: 376
- duration_s: 91.89526936174494
- tempo0: 65
- tempo_events: 5
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 11.75
- bar_density_p90: 18.7
- tracks: 2
- pitch_min: 40
- pitch_max: 95

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
- dynamic_windows: w00-w03:+12, w04-w04:+9, w05-w05:+12
- lead_notes: 138
- lead_from_melody_track: 134 (97.1%)
- lead_from_top_note: 138 (100.0%)
- fallback_lead_notes: 4
- lead_speed_pruned: 0
- support_notes_pruned: 5
- input_budget_dropped: 3

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 230.8
- same_key_min_gap_ms: 230.8
