# Analysis (Sky MelodyLock Human Script): xia-shan.mid

## Metrics
- note_count: 1411
- duration_s: 169.609756097561
- tempo0: 82
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 24.32758620689655
- bar_density_p90: 31.0
- tracks: 2
- pitch_min: 32
- pitch_max: 90

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
- base_shift: 8
- dynamic_windows: w00-w10:+8, w11-w11:+10, w12-w14:+7
- lead_notes: 532
- lead_from_melody_track: 531 (99.8%)
- lead_from_top_note: 528 (99.2%)
- fallback_lead_notes: 1
- lead_speed_pruned: 0
- support_notes_pruned: 189
- input_budget_dropped: 12

## Humanization Summary
- breath_hits: 72
- lag_hits: 11
- pocket_hits: 0
- release_hits: 2
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 182.9
- same_key_min_gap_ms: 182.9
