# Analysis (Sky MelodyLock Script): 四不可说.mid

## Metrics
- note_count: 287
- duration_s: 88.88828321054527
- tempo0: 62
- tempo_events: 5
- time_sig: 3/4
- max_poly: 7
- bar_density_mean: 9.89655172413793
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 36
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
- base_shift: 4
- dynamic_windows: w00-w03:+4, w04-w04:+1, w05-w05:+4
- lead_notes: 97
- lead_from_melody_track: 97 (100.0%)
- lead_from_top_note: 97 (100.0%)
- fallback_lead_notes: 0
- lead_speed_pruned: 0
- support_notes_pruned: 3
- input_budget_dropped: 1

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 241.9
- same_key_min_gap_ms: 241.9
