# Analysis (Guitar Literal Script): 01-xiao-xing-xing.mid

## Metrics
- note_count: 42
- duration_s: 24.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 1
- bar_density_mean: 3.5
- bar_density_p90: 4.0
- tracks: 1
- pitch_min: 69
- pitch_max: 78

## Conversion Snapshot
- top chord-zone usage: 0/24 (safe single-zone 24/24)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_strict
- reason: default guitar_literal_strict for maximal one-to-one feel

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
