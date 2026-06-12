# Analysis (Sky MelodyLock Script): happy-birthday-to-you-piano.mid

## Metrics
- note_count: 145
- duration_s: 28.45
- tempo0: 120
- tempo_events: 1
- time_sig: 1/4
- max_poly: 8
- bar_density_mean: 2.7358490566037736
- bar_density_p90: 4.0
- tracks: 2
- pitch_min: 48
- pitch_max: 82

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
- dynamic_windows: w00-w03:+12
- lead_notes: 57
- lead_from_melody_track: 57 (100.0%)
- lead_from_top_note: 57 (100.0%)
- fallback_lead_notes: 0
- lead_speed_pruned: 0
- support_notes_pruned: 3
- input_budget_dropped: 0

## Input Stability
- clusters_per_sec_peak: 3.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 500.0
