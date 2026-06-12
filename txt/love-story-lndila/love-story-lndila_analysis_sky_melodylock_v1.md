# Analysis (Sky MelodyLock Script): love-story-lndila.mid

## Metrics
- note_count: 1156
- duration_s: 116.25681414977689
- tempo0: 190
- tempo_events: 3
- time_sig: 3/4
- max_poly: 6
- bar_density_mean: 10.605504587155963
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 29
- pitch_max: 96

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
- dynamic_windows: w00-w20:+11
- lead_notes: 293
- lead_from_melody_track: 234 (79.9%)
- lead_from_top_note: 293 (100.0%)
- fallback_lead_notes: 59
- lead_speed_pruned: 0
- support_notes_pruned: 181
- input_budget_dropped: 14

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 97.4
- same_key_min_gap_ms: 157.9
