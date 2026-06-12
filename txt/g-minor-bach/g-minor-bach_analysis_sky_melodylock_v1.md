# Analysis (Sky MelodyLock Script): g-minor-bach.mid

## Metrics
- note_count: 1810
- duration_s: 158.28
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 27.424242424242426
- bar_density_p90: 34.0
- tracks: 3
- pitch_min: 34
- pitch_max: 80

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
- dynamic_windows: w00-w14:+9, w15-w16:+7
- lead_notes: 357
- lead_from_melody_track: 8 (2.2%)
- lead_from_top_note: 350 (98.0%)
- fallback_lead_notes: 349
- lead_speed_pruned: 0
- support_notes_pruned: 32
- input_budget_dropped: 16

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 150.0
- same_key_min_gap_ms: 150.0
