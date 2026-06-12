# Analysis (Sky MelodyLock Script): longing-inuyasha.mid

## Metrics
- note_count: 304
- duration_s: 96.0
- tempo0: 60
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 12.666666666666666
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 41
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
- base_shift: 12
- dynamic_windows: w00-w05:+12
- lead_notes: 134
- lead_from_melody_track: 133 (99.3%)
- lead_from_top_note: 134 (100.0%)
- fallback_lead_notes: 1
- lead_speed_pruned: 0
- support_notes_pruned: 29
- input_budget_dropped: 0

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 250.0
- same_key_min_gap_ms: 500.0
