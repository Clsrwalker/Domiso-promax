# Analysis (Sky MelodyLock Script): fan-wu-tuo-bang.mid

## Metrics
- note_count: 1140
- duration_s: 148.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.405405405405405
- bar_density_p90: 21.0
- tracks: 2
- pitch_min: 43
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
- dynamic_windows: w00-w04:+12, w05-w07:+10, w08-w18:+12
- lead_notes: 641
- lead_from_melody_track: 639 (99.7%)
- lead_from_top_note: 641 (100.0%)
- fallback_lead_notes: 2
- lead_speed_pruned: 0
- support_notes_pruned: 20
- input_budget_dropped: 28

## Input Stability
- clusters_per_sec_peak: 8.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
