# Analysis (Guitar Literal Script): 不要离开我青山黛玛.mid

## Metrics
- note_count: 1129
- duration_s: 232.7455357142857
- tempo0: 91
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 12.685393258426966
- bar_density_p90: 17.0
- tracks: 2
- pitch_min: 39
- pitch_max: 91

## Conversion Snapshot
- top chord-zone usage: 7/1653 (safe single-zone 1646/1653)
- chord pads injected: 6


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
