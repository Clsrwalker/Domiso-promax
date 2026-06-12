# Analysis (Sky MelodyLock Human Script): 将世事高枕.mid

## Metrics
- note_count: 679
- duration_s: 133.84855769230768
- tempo0: 104
- tempo_events: 2
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 11.912280701754385
- bar_density_p90: 17.4
- tracks: 2
- pitch_min: 37
- pitch_max: 87

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
- base_shift: 11
- dynamic_windows: w00-w07:+11, w08-w09:+8, w10-w14:+12
- lead_notes: 275
- lead_from_melody_track: 258 (93.8%)
- lead_from_top_note: 273 (99.3%)
- fallback_lead_notes: 17
- lead_speed_pruned: 0
- support_notes_pruned: 6
- input_budget_dropped: 3

## Humanization Summary
- breath_hits: 31
- lag_hits: 10
- pocket_hits: 0
- release_hits: 4
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 144.2
- same_key_min_gap_ms: 144.2
