# Analysis (Guitar Literal Script): Right Now (Na Na Na).mid

## Metrics
- note_count: 1471
- duration_s: 242.04144385026737
- tempo0: 136
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 10.737226277372264
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 40
- pitch_max: 78

## Conversion Snapshot
- top chord-zone usage: 47/1590 (safe single-zone 1543/1590)
- chord pads injected: 44


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
