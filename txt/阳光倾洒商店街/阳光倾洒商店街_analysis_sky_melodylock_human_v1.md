# Analysis (Sky MelodyLock Human Script): 阳光倾洒商店街.mid

## Metrics
- note_count: 1434
- duration_s: 114.64886934673366
- tempo0: 199
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 14.9375
- bar_density_p90: 19.3
- tracks: 2
- pitch_min: 43
- pitch_max: 91

## Recommended Profile
- sky_melodylock_human_dense
- reason: 15-key range + dense source -> sky_melodylock_human_dense

## Sky MelodyLock Human Intent
- keep Sky melodylock's recognizable top line and thin support structure
- add only light human timing, because Sky has tighter playable input limits than the 21-key scripts
- use phrase breath on melody, support lag behind the hook, short weak-tail release, and gradual rubato
- target layout: Y U I O P / H J K L ; / N M , . /

## Extraction Summary
- human_mode: lite
- human_desc: minimal humanization for Sky stability
- base_shift: 7
- dynamic_windows: w00-w06:+7, w07-w07:+4, w08-w23:+7
- lead_notes: 600
- lead_from_melody_track: 481 (80.2%)
- lead_from_top_note: 600 (100.0%)
- fallback_lead_notes: 119
- lead_speed_pruned: 25
- support_notes_pruned: 314
- input_budget_dropped: 39

## Humanization Summary
- breath_hits: 75
- lag_hits: 8
- pocket_hits: 0
- release_hits: 0
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 9.0
- min_cluster_gap_ms: 75.4
- same_key_min_gap_ms: 75.4
