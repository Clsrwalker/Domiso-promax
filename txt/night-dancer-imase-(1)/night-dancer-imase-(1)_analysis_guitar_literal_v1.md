# Analysis (Guitar Literal Script): night-dancer-imase (1).mid

## Metrics
- note_count: 2526
- duration_s: 208.47669491525423
- tempo0: 118
- tempo_events: 2
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 25.00990099009901
- bar_density_p90: 34.0
- tracks: 2
- pitch_min: 24
- pitch_max: 98

## Conversion Snapshot
- top chord-zone usage: 52/2763 (safe single-zone 2711/2763)
- chord pads injected: 47


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
