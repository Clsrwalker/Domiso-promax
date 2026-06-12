# Analysis (Sky MelodyLock Script): funeral-march.mid

## Metrics
- note_count: 2106
- duration_s: 539.875
- tempo0: 48
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 19.5
- bar_density_p90: 31.0
- tracks: 2
- pitch_min: 25
- pitch_max: 89

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
- dynamic_windows: w00-w26:+11
- lead_notes: 557
- lead_from_melody_track: 538 (96.6%)
- lead_from_top_note: 557 (100.0%)
- fallback_lead_notes: 19
- lead_speed_pruned: 0
- support_notes_pruned: 149
- input_budget_dropped: 47

## Input Stability
- clusters_per_sec_peak: 3.0
- min_cluster_gap_ms: 312.5
- same_key_min_gap_ms: 312.5
