# Analysis (Sky MelodyLock Script): windy-hill.mid

## Metrics
- note_count: 1515
- duration_s: 283.1666516635386
- tempo0: 74
- tempo_events: 8
- time_sig: 1/4
- max_poly: 6
- bar_density_mean: 4.40406976744186
- bar_density_p90: 7.0
- tracks: 2
- pitch_min: 35
- pitch_max: 93

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
- dynamic_windows: w00-w21:+10
- lead_notes: 641
- lead_from_melody_track: 619 (96.6%)
- lead_from_top_note: 641 (100.0%)
- fallback_lead_notes: 22
- lead_speed_pruned: 0
- support_notes_pruned: 11
- input_budget_dropped: 8

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 202.7
- same_key_min_gap_ms: 202.7
