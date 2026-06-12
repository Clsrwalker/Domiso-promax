# Analysis (Sky MelodyLock Script): 将世事高枕.mid

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
- sky_melodylock_dense
- reason: 15-key range + dense source -> sky_melodylock_dense

## Sky MelodyLock Intent
- preserve literal rhythm/body where possible, but lock Voice A to a singable lead line
- force output into Sky's 15-key C4-C6 layout
- keep the hook away from the lowest row when a better transpose exists
- keep support notes in B/C instead of letting A absorb the whole piano texture
- target layout: Y U I O P / H J K L ; / N M , . /

## Extraction Summary
- base_shift: 11
- dynamic_windows: w00-w07:+11, w08-w09:+8, w10-w14:+12
- lead_notes: 275
- lead_from_melody_track: 258 (93.8%)
- lead_from_top_note: 273 (99.3%)
- fallback_lead_notes: 17
- lead_speed_pruned: 0
- support_notes_pruned: 6
- input_budget_dropped: 7

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 144.2
- same_key_min_gap_ms: 144.2
