# Analysis (Sky MelodyLock Human Script): coldplay-viva-la-vida.mid

## Metrics
- note_count: 2658
- duration_s: 271.9
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.544117647058822
- bar_density_p90: 27.0
- tracks: 2
- pitch_min: 49
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
- dynamic_windows: w00-w33:+4
- lead_notes: 600
- lead_from_melody_track: 575 (95.8%)
- lead_from_top_note: 592 (98.7%)
- fallback_lead_notes: 25
- lead_speed_pruned: 0
- support_notes_pruned: 400
- input_budget_dropped: 17

## Humanization Summary
- breath_hits: 89
- lag_hits: 4
- pocket_hits: 0
- release_hits: 1
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 250.0
