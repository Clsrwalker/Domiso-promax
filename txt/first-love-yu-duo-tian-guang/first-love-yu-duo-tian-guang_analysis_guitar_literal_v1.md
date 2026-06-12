# Analysis (Guitar Literal Script): first-love-yu-duo-tian-guang.mid

## Metrics
- note_count: 1481
- duration_s: 225.6
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 15.75531914893617
- bar_density_p90: 23.0
- tracks: 2
- pitch_min: 31
- pitch_max: 91

## Conversion Snapshot
- top chord-zone usage: 46/1823 (safe single-zone 1777/1823)
- chord pads injected: 38


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
