# Analysis (Guitar Literal Script): golden-hour.mid

## Metrics
- note_count: 1073
- duration_s: 90.0
- tempo0: 96
- tempo_events: 1
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 44.708333333333336
- bar_density_p90: 59.0
- tracks: 2
- pitch_min: 40
- pitch_max: 92

## Conversion Snapshot
- top chord-zone usage: 7/1250 (safe single-zone 1243/1250)
- chord pads injected: 4


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
