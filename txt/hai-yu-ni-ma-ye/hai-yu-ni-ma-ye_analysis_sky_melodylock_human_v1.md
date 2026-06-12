# Analysis (Sky MelodyLock Human Script): hai-yu-ni-ma-ye.mid

## Metrics
- note_count: 1190
- duration_s: 308.57142857142856
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 13.370786516853933
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 34
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
- base_shift: 4
- dynamic_windows: w00-w14:+4, w15-w15:+1, w16-w22:+4
- lead_notes: 625
- lead_from_melody_track: 608 (97.3%)
- lead_from_top_note: 625 (100.0%)
- fallback_lead_notes: 17
- lead_speed_pruned: 0
- support_notes_pruned: 2
- input_budget_dropped: 5

## Humanization Summary
- breath_hits: 98
- lag_hits: 6
- pocket_hits: 0
- release_hits: 1
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 214.3
- same_key_min_gap_ms: 214.3
