# Analysis (Guitar Literal Script): uchiage-hanabi-fireworks-daoko.mid

## Metrics
- note_count: 2233
- duration_s: 283.891088014153
- tempo0: 95
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.9375
- bar_density_p90: 27.7
- tracks: 2
- pitch_min: 25
- pitch_max: 97

## Conversion Snapshot
- top chord-zone usage: 8/2638 (safe single-zone 2630/2638)
- chord pads injected: 8


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
