# Analysis (Guitar Literal Script): 遇见_孙燕姿.mid

## Metrics
- note_count: 1105
- duration_s: 193.54838709677418
- tempo0: 93
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 14.733333333333333
- bar_density_p90: 22.0
- tracks: 3
- pitch_min: 37
- pitch_max: 99

## Conversion Snapshot
- top chord-zone usage: 15/1462 (safe single-zone 1447/1462)
- chord pads injected: 14


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
