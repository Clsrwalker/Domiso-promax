# Analysis (Sky MelodyLock Human Script): fan-wu-tuo-bang.mid

## Metrics
- note_count: 1140
- duration_s: 148.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.405405405405405
- bar_density_p90: 21.0
- tracks: 2
- pitch_min: 43
- pitch_max: 79

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
- dynamic_windows: w00-w04:+12, w05-w07:+10, w08-w18:+12
- lead_notes: 641
- lead_from_melody_track: 639 (99.7%)
- lead_from_top_note: 641 (100.0%)
- fallback_lead_notes: 2
- lead_speed_pruned: 0
- support_notes_pruned: 20
- input_budget_dropped: 26

## Humanization Summary
- breath_hits: 57
- lag_hits: 13
- pocket_hits: 0
- release_hits: 3
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 7.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
