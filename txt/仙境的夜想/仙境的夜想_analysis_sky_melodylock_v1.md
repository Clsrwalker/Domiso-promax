# Analysis (Sky MelodyLock Script): 仙境的夜想.mid

## Metrics
- note_count: 522
- duration_s: 114.82931836057672
- tempo0: 137
- tempo_events: 9
- time_sig: 3/4
- max_poly: 6
- bar_density_mean: 6.0
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 34
- pitch_max: 97

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
- base_shift: 8
- dynamic_windows: w00-w08:+8, w09-w12:+6, w13-w16:+8
- lead_notes: 232
- lead_from_melody_track: 189 (81.5%)
- lead_from_top_note: 232 (100.0%)
- fallback_lead_notes: 43
- lead_speed_pruned: 0
- support_notes_pruned: 47
- input_budget_dropped: 8

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 109.5
- same_key_min_gap_ms: 438.0
