# Analysis (Sky Literal Script): runaway-aurora.mid

## Metrics
- note_count: 1802
- duration_s: 323.90643236074277
- tempo0: 58
- tempo_events: 2
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 15.669565217391304
- bar_density_p90: 26.8
- tracks: 2
- pitch_min: 28
- pitch_max: 99

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
- base_shift: 1
- dynamic_windows: w00-w21:+1
- lead_notes: 588
- lead_from_melody_track: 561 (95.4%)
- lead_from_top_note: 586 (99.7%)
- fallback_lead_notes: 27
- lead_speed_pruned: 0
- support_notes_pruned: 285
- input_budget_dropped: 21

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 230.8
- same_key_min_gap_ms: 230.8
