# Analysis (Sky MelodyLock Human Script): 如生之不竭.mid

## Metrics
- note_count: 1562
- duration_s: 151.69811320754715
- tempo0: 106
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 23.313432835820894
- bar_density_p90: 33.4
- tracks: 2
- pitch_min: 38
- pitch_max: 95

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
- base_shift: 12
- dynamic_windows: w00-w07:+12, w08-w11:+10, w12-w16:+12
- lead_notes: 699
- lead_from_melody_track: 667 (95.4%)
- lead_from_top_note: 694 (99.3%)
- fallback_lead_notes: 32
- lead_speed_pruned: 0
- support_notes_pruned: 208
- input_budget_dropped: 12

## Humanization Summary
- breath_hits: 58
- lag_hits: 14
- pocket_hits: 0
- release_hits: 1
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 8.0
- min_cluster_gap_ms: 141.5
- same_key_min_gap_ms: 141.5
