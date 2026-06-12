# Analysis (Sky MelodyLock Script): howls-moving-castle-main-theme.mid

## Metrics
- note_count: 2502
- duration_s: 306.99685998512393
- tempo0: 120
- tempo_events: 30
- time_sig: 3/4
- max_poly: 8
- bar_density_mean: 10.78448275862069
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 33
- pitch_max: 95

## Recommended Profile
- sky_melodylock_dense
- reason: 15-key range + dense source -> sky_melodylock_dense

## Sky MelodyLock Intent
- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line
- force output into Sky's 15-key C4-C6 layout
- keep the hook away from the lowest row when a better transpose exists
- keep support notes in B/C instead of letting A absorb the whole piano texture
- target layout: Y U I O P / H J K L ; / N M , . /

## Extraction Summary
- base_shift: 7
- dynamic_windows: w00-w33:+7, w34-w39:+5, w40-w43:+8
- lead_notes: 802
- lead_from_melody_track: 781 (97.4%)
- lead_from_top_note: 801 (99.9%)
- fallback_lead_notes: 21
- lead_speed_pruned: 0
- support_notes_pruned: 128
- input_budget_dropped: 97

## Input Stability
- clusters_per_sec_peak: 10.0
- min_cluster_gap_ms: 91.5
- same_key_min_gap_ms: 138.9
