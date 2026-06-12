# Analysis (Sky MelodyLock Script): higher-tobu.mid

## Metrics
- note_count: 2175
- duration_s: 208.7359866220736
- tempo0: 130
- tempo_events: 7
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.419642857142858
- bar_density_p90: 24.7
- tracks: 5
- pitch_min: 36
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
- base_shift: 5
- dynamic_windows: w00-w27:+5
- lead_notes: 705
- lead_from_melody_track: 215 (30.5%)
- lead_from_top_note: 686 (97.3%)
- fallback_lead_notes: 490
- lead_speed_pruned: 0
- support_notes_pruned: 580
- input_budget_dropped: 8

## Input Stability
- clusters_per_sec_peak: 8.0
- min_cluster_gap_ms: 115.4
- same_key_min_gap_ms: 115.4
