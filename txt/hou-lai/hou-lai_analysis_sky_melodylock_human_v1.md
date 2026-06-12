# Analysis (Sky MelodyLock Human Script): hou-lai.mid

## Metrics
- note_count: 1465
- duration_s: 316.8
- tempo0: 75
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 14.797979797979798
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 24
- pitch_max: 98

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
- base_shift: 9
- dynamic_windows: w00-w24:+9
- lead_notes: 567
- lead_from_melody_track: 542 (95.6%)
- lead_from_top_note: 567 (100.0%)
- fallback_lead_notes: 25
- lead_speed_pruned: 0
- support_notes_pruned: 6
- input_budget_dropped: 5

## Humanization Summary
- breath_hits: 84
- lag_hits: 10
- pocket_hits: 0
- release_hits: 1
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 200.0
- same_key_min_gap_ms: 200.0
