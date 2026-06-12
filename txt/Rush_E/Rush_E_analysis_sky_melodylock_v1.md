# Analysis (Sky MelodyLock Script): Rush_E.mid

## Metrics
- note_count: 1842
- duration_s: 179.43580538189738
- tempo0: 70
- tempo_events: 186
- time_sig: 4/4
- max_poly: 57
- bar_density_mean: 11.883870967741936
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 25
- pitch_max: 108

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
- dynamic_windows: w00-w33:+12, w34-w38:+11
- lead_notes: 835
- lead_from_melody_track: 768 (92.0%)
- lead_from_top_note: 833 (99.8%)
- fallback_lead_notes: 67
- lead_speed_pruned: 0
- support_notes_pruned: 25
- input_budget_dropped: 64

## Input Stability
- clusters_per_sec_peak: 11.0
- min_cluster_gap_ms: 45.5
- same_key_min_gap_ms: 94.6
