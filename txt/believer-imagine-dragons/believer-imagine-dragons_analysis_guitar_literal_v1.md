# Analysis (Guitar Literal Script): believer-imagine-dragons.mid

## Metrics
- note_count: 1468
- duration_s: 191.4900265957447
- tempo0: 188
- tempo_events: 1
- time_sig: 12/8
- max_poly: 4
- bar_density_mean: 14.68
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 34
- pitch_max: 85

## Conversion Snapshot
- top chord-zone usage: 127/1762 (safe single-zone 1635/1762)
- chord pads injected: 116


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
