# Analysis (Guitar Literal Script): 春泥_池魚.mid

## Metrics
- note_count: 746
- duration_s: 200.87984742530196
- tempo0: 143
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 6.26890756302521
- bar_density_p90: 8.0
- tracks: 2
- pitch_min: 36
- pitch_max: 84

## Conversion Snapshot
- top chord-zone usage: 102/1647 (safe single-zone 1545/1647)
- chord pads injected: 89


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
