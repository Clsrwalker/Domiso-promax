# Analysis (Guitar Literal Script): 人鱼湾音乐夜晚变奏.mid

## Metrics
- note_count: 359
- duration_s: 103.04086538461539
- tempo0: 91
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 8.975
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 41
- pitch_max: 96

## Conversion Snapshot
- top chord-zone usage: 16/679 (safe single-zone 663/679)
- chord pads injected: 11


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
