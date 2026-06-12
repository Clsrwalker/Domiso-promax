# Analysis (Sky Literal Script): czardas.mid

## Metrics
- note_count: 2403
- duration_s: 268.61831376129766
- tempo0: 55
- tempo_events: 15
- time_sig: 2/4
- max_poly: 8
- bar_density_mean: 12.075376884422111
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 31
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
- base_shift: 12
- dynamic_windows: w00-w14:+12, w15-w24:+10
- lead_notes: 979
- lead_from_melody_track: 937 (95.7%)
- lead_from_top_note: 979 (100.0%)
- fallback_lead_notes: 42
- lead_speed_pruned: 0
- support_notes_pruned: 48
- input_budget_dropped: 43

## Input Stability
- clusters_per_sec_peak: 11.0
- min_cluster_gap_ms: 92.6
- same_key_min_gap_ms: 107.1
