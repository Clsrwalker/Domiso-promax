# Analysis (Sky MelodyLock Human Script): 仙境的夜想.mid

## Metrics
- note_count: 522
- duration_s: 114.82931836057672
- tempo0: 137
- tempo_events: 9
- time_sig: 3/4
- max_poly: 6
- bar_density_mean: 6.0
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 34
- pitch_max: 97

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
- dynamic_windows: w00-w08:+8, w09-w12:+6, w13-w16:+8
- lead_notes: 232
- lead_from_melody_track: 189 (81.5%)
- lead_from_top_note: 232 (100.0%)
- fallback_lead_notes: 43
- lead_speed_pruned: 0
- support_notes_pruned: 47
- input_budget_dropped: 8

## Humanization Summary
- breath_hits: 41
- lag_hits: 16
- pocket_hits: 0
- release_hits: 0
- rubato_depth_bpm: 1

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 109.5
- same_key_min_gap_ms: 328.5
