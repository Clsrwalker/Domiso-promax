# Analysis (Sky MelodyLock Script): ai-he-jiang-xue-er.mid

## Metrics
- note_count: 1017
- duration_s: 220.0
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.646153846153846
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 39
- pitch_max: 83

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
- base_shift: 1
- dynamic_windows: w00-w15:+1, w16-w16:-2
- lead_notes: 483
- lead_from_melody_track: 476 (98.6%)
- lead_from_top_note: 483 (100.0%)
- fallback_lead_notes: 7
- lead_speed_pruned: 0
- support_notes_pruned: 0
- input_budget_dropped: 12

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 208.3
- same_key_min_gap_ms: 208.3
