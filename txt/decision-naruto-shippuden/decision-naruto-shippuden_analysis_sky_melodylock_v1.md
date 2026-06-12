# Analysis (Sky MelodyLock Script): decision-naruto-shippuden.mid

## Metrics
- note_count: 153
- duration_s: 180.0
- tempo0: 60
- tempo_events: 1
- time_sig: 4/4
- max_poly: 1
- bar_density_mean: 3.4
- bar_density_p90: 5.0
- tracks: 1
- pitch_min: 60
- pitch_max: 83

## Recommended Profile
- sky_melodylock
- reason: default Sky melodylock profile

## Sky MelodyLock Intent
- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line
- force output into Sky's 15-key C4-C6 layout
- keep the hook away from the lowest row when a better transpose exists
- keep support notes in B/C instead of letting A absorb the whole piano texture
- target layout: Y U I O P / H J K L ; / N M , . /

## Extraction Summary
- base_shift: 5
- dynamic_windows: w00-w03:+7, w04-w11:+5
- lead_notes: 153
- lead_from_melody_track: 153 (100.0%)
- lead_from_top_note: 153 (100.0%)
- fallback_lead_notes: 0
- lead_speed_pruned: 0
- support_notes_pruned: 0
- input_budget_dropped: 0

## Input Stability
- clusters_per_sec_peak: 3.0
- min_cluster_gap_ms: 500.0
- same_key_min_gap_ms: 1000.0
