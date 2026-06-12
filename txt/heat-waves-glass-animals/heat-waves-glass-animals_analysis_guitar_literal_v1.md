# Analysis (Guitar Literal Script): heat-waves-glass-animals.mid

## Metrics
- note_count: 1593
- duration_s: 219.08333333333331
- tempo0: 81
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 21.82191780821918
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 28
- pitch_max: 87

## Conversion Snapshot
- top chord-zone usage: 1/1550 (safe single-zone 1549/1550)
- chord pads injected: 1


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
