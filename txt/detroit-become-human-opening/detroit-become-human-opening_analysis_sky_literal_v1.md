# Analysis (Sky Literal Script): detroit-become-human-opening.mid

## Metrics
- note_count: 586
- duration_s: 100.00208333333333
- tempo0: 60
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.44
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 36
- pitch_max: 88

## Recommended Profile
- sky_literal_dense
- reason: 15-key range + dense source -> sky_literal_dense

## Sky Literal Intent
- preserve more literal rhythm/body than sky melodylock while keeping Voice A singable
- force output into Sky's 15-key C4-C6 layout
- keep bass and key inner motions that help recognize the original arrangement
- trim same-tick middle clutter before it turns into mush on Sky input
- target layout: Y U I O P / H J K L ; / N M , . /

## Extraction Summary
- base_shift: 10
- dynamic_windows: w00-w02:+12, w03-w04:+10, w05-w06:+12
- lead_notes: 238
- lead_from_melody_track: 232 (97.5%)
- lead_from_top_note: 238 (100.0%)
- fallback_lead_notes: 6
- lead_speed_pruned: 0
- support_notes_pruned: 166
- input_budget_dropped: 6

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 250.0
- same_key_min_gap_ms: 500.0
