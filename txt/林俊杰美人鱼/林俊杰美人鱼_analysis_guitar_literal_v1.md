# Analysis (Guitar Literal Script): 林俊杰美人鱼.mid

## Metrics
- note_count: 1106
- duration_s: 251.57930367504835
- tempo0: 94
- tempo_events: 1
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 11.171717171717171
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 36
- pitch_max: 83

## Conversion Snapshot
- top chord-zone usage: 12/1343 (safe single-zone 1331/1343)
- chord pads injected: 12


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
