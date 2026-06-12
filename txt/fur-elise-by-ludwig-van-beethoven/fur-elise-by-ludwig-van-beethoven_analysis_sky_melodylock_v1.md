# Analysis (Sky MelodyLock Script): fur-elise-by-ludwig-van-beethoven.mid

## Metrics
- note_count: 1041
- duration_s: 94.0
- tempo0: 120
- tempo_events: 1
- time_sig: 1/8
- max_poly: 6
- bar_density_mean: 2.783422459893048
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 33
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
- base_shift: 12
- dynamic_windows: w00-w11:+12
- lead_notes: 527
- lead_from_melody_track: 497 (94.3%)
- lead_from_top_note: 527 (100.0%)
- fallback_lead_notes: 30
- lead_speed_pruned: 0
- support_notes_pruned: 49
- input_budget_dropped: 3

## Input Stability
- clusters_per_sec_peak: 9.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
