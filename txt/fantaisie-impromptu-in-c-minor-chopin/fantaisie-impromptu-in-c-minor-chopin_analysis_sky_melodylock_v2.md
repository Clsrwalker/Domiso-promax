# Analysis (Sky MelodyLock Script): fantaisie-impromptu-in-c-minor-chopin.mid

## Metrics
- note_count: 3049
- duration_s: 327.51022460328124
- tempo0: 168
- tempo_events: 38
- time_sig: 2/2
- max_poly: 6
- bar_density_mean: 22.094202898550726
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 100

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
- dynamic_windows: w00-w09:+8, w10-w19:+6, w20-w34:+8
- lead_notes: 1663
- lead_from_melody_track: 1605 (96.5%)
- lead_from_top_note: 1663 (100.0%)
- fallback_lead_notes: 58
- lead_speed_pruned: 0
- support_notes_pruned: 365
- input_budget_dropped: 161

## Input Stability
- clusters_per_sec_peak: 12.0
- min_cluster_gap_ms: 89.3
- same_key_min_gap_ms: 89.3
