# Analysis (Sky MelodyLock Script): my-heart-will-go-on.mid

## Metrics
- note_count: 1451
- duration_s: 285.59999999999997
- tempo0: 90
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 12.296610169491526
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 37
- pitch_max: 88

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
- base_shift: 8
- dynamic_windows: w00-w22:+8, w23-w29:+9
- lead_notes: 413
- lead_from_melody_track: 368 (89.1%)
- lead_from_top_note: 408 (98.8%)
- fallback_lead_notes: 45
- lead_speed_pruned: 0
- support_notes_pruned: 114
- input_budget_dropped: 5

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 150.0
- same_key_min_gap_ms: 150.0
