# Analysis (Sky MelodyLock Script): luv-letter.mid

## Metrics
- note_count: 1921
- duration_s: 295.4516979600596
- tempo0: 80
- tempo_events: 15
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.404040404040405
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 34
- pitch_max: 101

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
- base_shift: 11
- dynamic_windows: w00-w24:+11
- lead_notes: 927
- lead_from_melody_track: 907 (97.8%)
- lead_from_top_note: 927 (100.0%)
- fallback_lead_notes: 20
- lead_speed_pruned: 0
- support_notes_pruned: 117
- input_budget_dropped: 35

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 100.0
- same_key_min_gap_ms: 154.6
