# Analysis (Sky Literal Script): fur-elise-beethoven.mid

## Metrics
- note_count: 1040
- duration_s: 156.83901515151518
- tempo0: 72
- tempo_events: 2
- time_sig: 1/8
- max_poly: 6
- bar_density_mean: 2.7807486631016043
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 33
- pitch_max: 100

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
- dynamic_windows: w00-w11:+12
- lead_notes: 533
- lead_from_melody_track: 502 (94.2%)
- lead_from_top_note: 533 (100.0%)
- fallback_lead_notes: 31
- lead_speed_pruned: 0
- support_notes_pruned: 291
- input_budget_dropped: 4

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 208.3
- same_key_min_gap_ms: 208.3
