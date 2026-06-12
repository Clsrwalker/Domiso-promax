# Analysis (Sky MelodyLock Script): numb-linkin-park.mid

## Metrics
- note_count: 1271
- duration_s: 176.61818181818182
- tempo0: 110
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.691358024691358
- bar_density_p90: 21.8
- tracks: 2
- pitch_min: 41
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
- dynamic_windows: w00-w20:+7
- lead_notes: 413
- lead_from_melody_track: 393 (95.2%)
- lead_from_top_note: 413 (100.0%)
- fallback_lead_notes: 20
- lead_speed_pruned: 0
- support_notes_pruned: 204
- input_budget_dropped: 84

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 136.4
- same_key_min_gap_ms: 272.7
