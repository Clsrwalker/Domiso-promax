# Analysis (Sky MelodyLock Human Script): beethoven-virus-piano.mid

## Metrics
- note_count: 2671
- duration_s: 216.73125
- tempo0: 160
- tempo_events: 3
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.07857142857143
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 21
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
- dynamic_windows: w00-w29:+12, w30-w34:+9
- lead_notes: 1069
- lead_from_melody_track: 1012 (94.7%)
- lead_from_top_note: 1065 (99.6%)
- fallback_lead_notes: 57
- lead_speed_pruned: 0
- support_notes_pruned: 189
- input_budget_dropped: 119

## Humanization Summary
- breath_hits: 106
- lag_hits: 15
- pocket_hits: 0
- release_hits: 1
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 11.0
- min_cluster_gap_ms: 93.8
- same_key_min_gap_ms: 187.5
