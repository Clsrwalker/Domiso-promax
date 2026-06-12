# Analysis (Sky MelodyLock Script): ballade-pour-adeline-richard-clayderman.mid

## Metrics
- note_count: 912
- duration_s: 174.7543530772633
- tempo0: 60
- tempo_events: 11
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 21.209302325581394
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 93

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
- dynamic_windows: w00-w10:+12
- lead_notes: 390
- lead_from_melody_track: 352 (90.3%)
- lead_from_top_note: 390 (100.0%)
- fallback_lead_notes: 38
- lead_speed_pruned: 0
- support_notes_pruned: 41
- input_budget_dropped: 7

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 250.0
- same_key_min_gap_ms: 250.0
