# Analysis (Sky MelodyLock Script): hai-yu-ni-ma-ye.mid

## Metrics
- note_count: 1190
- duration_s: 308.57142857142856
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 13.370786516853933
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 34
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
- base_shift: 4
- dynamic_windows: w00-w14:+4, w15-w15:+1, w16-w22:+4
- lead_notes: 625
- lead_from_melody_track: 608 (97.3%)
- lead_from_top_note: 625 (100.0%)
- fallback_lead_notes: 17
- lead_speed_pruned: 0
- support_notes_pruned: 2
- input_budget_dropped: 5

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 214.3
- same_key_min_gap_ms: 214.3
