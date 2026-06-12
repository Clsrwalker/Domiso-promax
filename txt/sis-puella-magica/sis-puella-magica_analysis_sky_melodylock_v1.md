# Analysis (Sky MelodyLock Script): sis-puella-magica.mid

## Metrics
- note_count: 1713
- duration_s: 153.16607862903226
- tempo0: 155
- tempo_events: 3
- time_sig: 3/4
- max_poly: 7
- bar_density_mean: 13.279069767441861
- bar_density_p90: 17.0
- tracks: 4
- pitch_min: 31
- pitch_max: 94

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
- base_shift: 7
- dynamic_windows: w00-w24:+7
- lead_notes: 462
- lead_from_melody_track: 326 (70.6%)
- lead_from_top_note: 451 (97.6%)
- fallback_lead_notes: 136
- lead_speed_pruned: 0
- support_notes_pruned: 151
- input_budget_dropped: 36

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 96.8
- same_key_min_gap_ms: 193.5
