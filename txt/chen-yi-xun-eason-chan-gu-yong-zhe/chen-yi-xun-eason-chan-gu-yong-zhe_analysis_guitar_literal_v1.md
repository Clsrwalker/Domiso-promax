# Analysis (Guitar Literal Script): chen-yi-xun-eason-chan-gu-yong-zhe.mid

## Metrics
- note_count: 1745
- duration_s: 254.97656250000003
- tempo0: 64
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 25.66176470588235
- bar_density_p90: 41.2
- tracks: 2
- pitch_min: 25
- pitch_max: 94

## Conversion Snapshot
- top chord-zone usage: 9/1727 (safe single-zone 1718/1727)
- chord pads injected: 8


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
