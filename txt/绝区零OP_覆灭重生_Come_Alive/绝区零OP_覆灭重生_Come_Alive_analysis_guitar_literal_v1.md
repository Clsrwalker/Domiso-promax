# Analysis (Guitar Literal Script): 绝区零OP_覆灭重生_Come_Alive.mid

## Metrics
- note_count: 1130
- duration_s: 238.56013551665723
- tempo0: 161
- tempo_events: 1
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 7.0625
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 26
- pitch_max: 79

## Conversion Snapshot
- top chord-zone usage: 85/1526 (safe single-zone 1441/1526)
- chord pads injected: 78


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
