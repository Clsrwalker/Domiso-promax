# Analysis (Sky MelodyLock Script): rolling-in-the-deep-adele.mid

## Metrics
- note_count: 1007
- duration_s: 127.09499999999998
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.0
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 43
- pitch_max: 86

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
- dynamic_windows: w00-w13:+9
- lead_notes: 321
- lead_from_melody_track: 298 (92.8%)
- lead_from_top_note: 321 (100.0%)
- fallback_lead_notes: 23
- lead_speed_pruned: 0
- support_notes_pruned: 111
- input_budget_dropped: 1

## Input Stability
- clusters_per_sec_peak: 4.0
- min_cluster_gap_ms: 150.0
- same_key_min_gap_ms: 150.0
