# Analysis (Sky MelodyLock Script): Beyond - 海阔天空.mid

## Metrics
- note_count: 2108
- duration_s: 343.33333333333337
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 14
- bar_density_mean: 20.466019417475728
- bar_density_p90: 35.6
- tracks: 2
- pitch_min: 36
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
- base_shift: 12
- dynamic_windows: w00-w13:+12, w14-w14:+10, w15-w25:+12
- lead_notes: 699
- lead_from_melody_track: 667 (95.4%)
- lead_from_top_note: 681 (97.4%)
- fallback_lead_notes: 32
- lead_speed_pruned: 0
- support_notes_pruned: 247
- input_budget_dropped: 55

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 208.3
- same_key_min_gap_ms: 208.3
