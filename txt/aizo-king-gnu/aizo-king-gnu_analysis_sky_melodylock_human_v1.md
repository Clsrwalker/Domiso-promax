# Analysis (Sky MelodyLock Human Script): aizo-king-gnu.mid

## Metrics
- note_count: 1237
- duration_s: 86.84210526315789
- tempo0: 190
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.92753623188406
- bar_density_p90: 25.0
- tracks: 2
- pitch_min: 33
- pitch_max: 100

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
- dynamic_windows: w00-w17:+12
- lead_notes: 465
- lead_from_melody_track: 444 (95.5%)
- lead_from_top_note: 459 (98.7%)
- fallback_lead_notes: 21
- lead_speed_pruned: 53
- support_notes_pruned: 157
- input_budget_dropped: 52

## Humanization Summary
- breath_hits: 65
- lag_hits: 18
- pocket_hits: 0
- release_hits: 3
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 9.0
- min_cluster_gap_ms: 78.9
- same_key_min_gap_ms: 157.9
