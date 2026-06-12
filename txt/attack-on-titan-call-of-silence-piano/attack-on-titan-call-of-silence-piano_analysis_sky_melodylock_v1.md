# Analysis (Sky MelodyLock Script): attack-on-titan-call-of-silence-piano.mid

## Metrics
- note_count: 689
- duration_s: 137.00104166666668
- tempo0: 120
- tempo_events: 1
- time_sig: 2/4
- max_poly: 8
- bar_density_mean: 5.0661764705882355
- bar_density_p90: 10.0
- tracks: 2
- pitch_min: 25
- pitch_max: 93

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
- base_shift: 3
- dynamic_windows: w00-w16:+3
- lead_notes: 199
- lead_from_melody_track: 145 (72.9%)
- lead_from_top_note: 199 (100.0%)
- fallback_lead_notes: 54
- lead_speed_pruned: 0
- support_notes_pruned: 19
- input_budget_dropped: 44

## Input Stability
- clusters_per_sec_peak: 5.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 250.0
