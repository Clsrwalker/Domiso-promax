# Analysis (Sky MelodyLock Human Script): ni-de-bei-bao.mid

## Metrics
- note_count: 1325
- duration_s: 205.53214285714284
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 22.45762711864407
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 25
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
- base_shift: 8
- dynamic_windows: w00-w09:+8, w10-w10:+10, w11-w14:+8
- lead_notes: 437
- lead_from_melody_track: 412 (94.3%)
- lead_from_top_note: 437 (100.0%)
- fallback_lead_notes: 25
- lead_speed_pruned: 0
- support_notes_pruned: 14
- input_budget_dropped: 12

## Humanization Summary
- breath_hits: 40
- lag_hits: 5
- pocket_hits: 0
- release_hits: 1
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 214.3
- same_key_min_gap_ms: 214.3
