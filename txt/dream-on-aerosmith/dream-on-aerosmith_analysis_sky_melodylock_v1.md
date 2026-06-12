# Analysis (Sky MelodyLock Script): dream-on-aerosmith.mid

## Metrics
- note_count: 2020
- duration_s: 261.53685897435895
- tempo0: 78
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 24.047619047619047
- bar_density_p90: 34.0
- tracks: 2
- pitch_min: 29
- pitch_max: 92

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
- dynamic_windows: w00-w20:+9
- lead_notes: 710
- lead_from_melody_track: 693 (97.6%)
- lead_from_top_note: 710 (100.0%)
- fallback_lead_notes: 17
- lead_speed_pruned: 0
- support_notes_pruned: 204
- input_budget_dropped: 8

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 192.3
- same_key_min_gap_ms: 192.3
