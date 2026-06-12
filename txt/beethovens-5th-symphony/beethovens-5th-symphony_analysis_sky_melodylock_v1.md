# Analysis (Sky MelodyLock Script): beethovens-5th-symphony.mid

## Metrics
- note_count: 2834
- duration_s: 151.76999999999998
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 44.28125
- bar_density_p90: 122.5
- tracks: 2
- pitch_min: 26
- pitch_max: 91

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
- dynamic_windows: w00-w04:+9, w05-w05:+11, w06-w15:+9
- lead_notes: 688
- lead_from_melody_track: 668 (97.1%)
- lead_from_top_note: 688 (100.0%)
- fallback_lead_notes: 20
- lead_speed_pruned: 0
- support_notes_pruned: 938
- input_budget_dropped: 19

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 150.0
- same_key_min_gap_ms: 150.0
