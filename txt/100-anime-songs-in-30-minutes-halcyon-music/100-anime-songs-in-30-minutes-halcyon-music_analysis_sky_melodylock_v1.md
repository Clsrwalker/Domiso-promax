# Analysis (Sky MelodyLock Script): 100-anime-songs-in-30-minutes-halcyon-music.mid

## Metrics
- note_count: 17149
- duration_s: 1725.450325619463
- tempo0: 80
- tempo_events: 66
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 15.463480613165013
- bar_density_p90: 23.0
- tracks: 2
- pitch_min: 23
- pitch_max: 94

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
- dynamic_windows: w00-w155:+12, w156-w207:+11, w208-w277:+10
- lead_notes: 5589
- lead_from_melody_track: 5218 (93.4%)
- lead_from_top_note: 5560 (99.5%)
- fallback_lead_notes: 371
- lead_speed_pruned: 5
- support_notes_pruned: 2310
- input_budget_dropped: 247

## Input Stability
- clusters_per_sec_peak: 11.0
- min_cluster_gap_ms: 83.3
- same_key_min_gap_ms: 103.4
