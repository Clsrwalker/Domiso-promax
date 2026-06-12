# Analysis (Sky Literal Script): Wedding_March_Mendelssohn_Piano.mid

## Metrics
- note_count: 4617
- duration_s: 294.64000000000004
- tempo0: 150
- tempo_events: 1
- time_sig: 1/4
- max_poly: 7
- bar_density_mean: 6.324657534246575
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 26
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
- dynamic_windows: w00-w16:+12, w17-w19:+10, w20-w45:+12
- lead_notes: 1045
- lead_from_melody_track: 1010 (96.7%)
- lead_from_top_note: 1017 (97.3%)
- fallback_lead_notes: 35
- lead_speed_pruned: 0
- support_notes_pruned: 199
- input_budget_dropped: 194

## Input Stability
- clusters_per_sec_peak: 11.0
- min_cluster_gap_ms: 100.0
- same_key_min_gap_ms: 100.0
