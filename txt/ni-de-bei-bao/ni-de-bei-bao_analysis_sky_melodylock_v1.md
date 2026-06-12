# Analysis (Sky MelodyLock Script): ni-de-bei-bao.mid

## Metrics
- note_count: 1325
- duration_s: 205.53214285714284
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 22.45762711864407
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 25
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
- base_shift: 8
- dynamic_windows: w00-w09:+8, w10-w10:+10, w11-w14:+8
- lead_notes: 437
- lead_from_melody_track: 412 (94.3%)
- lead_from_top_note: 437 (100.0%)
- fallback_lead_notes: 25
- lead_speed_pruned: 0
- support_notes_pruned: 14
- input_budget_dropped: 12

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 214.3
- same_key_min_gap_ms: 214.3
