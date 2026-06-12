# Analysis (Sky MelodyLock Human Script): czardas.mid

## Metrics
- note_count: 2403
- duration_s: 268.61831376129766
- tempo0: 55
- tempo_events: 15
- time_sig: 2/4
- max_poly: 8
- bar_density_mean: 12.075376884422111
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 31
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
- base_shift: 12
- dynamic_windows: w00-w14:+12, w15-w24:+10
- lead_notes: 979
- lead_from_melody_track: 937 (95.7%)
- lead_from_top_note: 979 (100.0%)
- fallback_lead_notes: 42
- lead_speed_pruned: 0
- support_notes_pruned: 108
- input_budget_dropped: 30

## Humanization Summary
- breath_hits: 69
- lag_hits: 9
- pocket_hits: 0
- release_hits: 0
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 10.0
- min_cluster_gap_ms: 92.6
- same_key_min_gap_ms: 166.7
