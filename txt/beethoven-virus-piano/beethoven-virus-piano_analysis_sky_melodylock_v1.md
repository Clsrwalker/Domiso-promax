# Analysis (Sky MelodyLock Script): beethoven-virus-piano.mid

## Metrics
- note_count: 2671
- duration_s: 216.73125
- tempo0: 160
- tempo_events: 3
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.07857142857143
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 21
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
- dynamic_windows: w00-w29:+12, w30-w34:+9
- lead_notes: 1069
- lead_from_melody_track: 1012 (94.7%)
- lead_from_top_note: 1065 (99.6%)
- fallback_lead_notes: 57
- lead_speed_pruned: 0
- support_notes_pruned: 189
- input_budget_dropped: 171

## Input Stability
- clusters_per_sec_peak: 11.0
- min_cluster_gap_ms: 93.8
- same_key_min_gap_ms: 187.5
