# Analysis (Sky MelodyLock Human Script): detroit-become-human-opening.mid

## Metrics
- note_count: 586
- duration_s: 100.00208333333333
- tempo0: 60
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.44
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 36
- pitch_max: 88

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
- base_shift: 10
- dynamic_windows: w00-w02:+12, w03-w04:+10, w05-w06:+12
- lead_notes: 238
- lead_from_melody_track: 232 (97.5%)
- lead_from_top_note: 238 (100.0%)
- fallback_lead_notes: 6
- lead_speed_pruned: 0
- support_notes_pruned: 171
- input_budget_dropped: 6

## Humanization Summary
- breath_hits: 13
- lag_hits: 1
- pocket_hits: 0
- release_hits: 0
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 4.0
- min_cluster_gap_ms: 250.0
- same_key_min_gap_ms: 508.5
