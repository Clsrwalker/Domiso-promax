# Analysis (Sky MelodyLock Script): detective-conan-main-theme.mid

## Metrics
- note_count: 2224
- duration_s: 184.87263858897362
- tempo0: 145
- tempo_events: 4
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 21.59223300970874
- bar_density_p90: 28.6
- tracks: 2
- pitch_min: 24
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
- base_shift: 4
- dynamic_windows: w00-w25:+4
- lead_notes: 701
- lead_from_melody_track: 658 (93.9%)
- lead_from_top_note: 695 (99.1%)
- fallback_lead_notes: 43
- lead_speed_pruned: 0
- support_notes_pruned: 246
- input_budget_dropped: 91

## Input Stability
- clusters_per_sec_peak: 10.0
- min_cluster_gap_ms: 103.4
- same_key_min_gap_ms: 107.1
