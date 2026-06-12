# Analysis (Sky MelodyLock Script): stitches.mid

## Metrics
- note_count: 513
- duration_s: 74.4
- tempo0: 145
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 11.4
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 38
- pitch_max: 79

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
- lead_notes: 189
- lead_from_melody_track: 147 (77.8%)
- lead_from_top_note: 187 (98.9%)
- fallback_lead_notes: 42
- lead_speed_pruned: 0
- support_notes_pruned: 2
- input_budget_dropped: 9

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 103.4
- same_key_min_gap_ms: 206.9
