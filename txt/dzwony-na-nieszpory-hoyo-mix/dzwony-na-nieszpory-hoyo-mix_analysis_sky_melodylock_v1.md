# Analysis (Sky MelodyLock Script): dzwony-na-nieszpory-hoyo-mix.mid

## Metrics
- note_count: 722
- duration_s: 98.06650901373021
- tempo0: 120
- tempo_events: 4
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 11.107692307692307
- bar_density_p90: 19.0
- tracks: 4
- pitch_min: 36
- pitch_max: 88

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
- base_shift: 12
- dynamic_windows: w00-w12:+12
- lead_notes: 279
- lead_from_melody_track: 105 (37.6%)
- lead_from_top_note: 271 (97.1%)
- fallback_lead_notes: 174
- lead_speed_pruned: 0
- support_notes_pruned: 105
- input_budget_dropped: 21

## Input Stability
- clusters_per_sec_peak: 6.0
- min_cluster_gap_ms: 125.0
- same_key_min_gap_ms: 125.0
