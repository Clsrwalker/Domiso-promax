# Analysis (Sky MelodyLock Human Script): mystery-of-love.mid

## Metrics
- note_count: 1571
- duration_s: 201.85
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.71
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 47
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
- dynamic_windows: w00-w20:+10, w21-w23:+12, w24-w24:+10
- lead_notes: 427
- lead_from_melody_track: 410 (96.0%)
- lead_from_top_note: 427 (100.0%)
- fallback_lead_notes: 17
- lead_speed_pruned: 0
- support_notes_pruned: 8
- input_budget_dropped: 2

## Humanization Summary
- breath_hits: 72
- lag_hits: 25
- pocket_hits: 0
- release_hits: 2
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 8.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
