# Analysis (Sky Literal Script): coldplay-viva-la-vida.mid

## Metrics
- note_count: 2658
- duration_s: 271.9
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.544117647058822
- bar_density_p90: 27.0
- tracks: 2
- pitch_min: 49
- pitch_max: 91

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
- base_shift: 4
- dynamic_windows: w00-w33:+4
- lead_notes: 600
- lead_from_melody_track: 575 (95.8%)
- lead_from_top_note: 592 (98.7%)
- fallback_lead_notes: 25
- lead_speed_pruned: 0
- support_notes_pruned: 159
- input_budget_dropped: 10

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 250.0
- same_key_min_gap_ms: 250.0
