# Analysis (Sky Literal Script): moonlight-sonata-i.mid

## Metrics
- note_count: 1164
- duration_s: 368.0027777777778
- tempo0: 45
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 16.869565217391305
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 29
- pitch_max: 87

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
- base_shift: 8
- dynamic_windows: w00-w01:+8, w02-w04:+10, w05-w17:+8
- lead_notes: 807
- lead_from_melody_track: 802 (99.4%)
- lead_from_top_note: 807 (100.0%)
- fallback_lead_notes: 5
- lead_speed_pruned: 0
- support_notes_pruned: 30
- input_budget_dropped: 51

## Input Stability
- clusters_per_sec_peak: 3.0
- min_cluster_gap_ms: 333.3
- same_key_min_gap_ms: 333.3
