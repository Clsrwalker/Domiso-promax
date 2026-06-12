# Analysis (Guitar Literal Script): all-of-me-violin.mid

## Metrics
- note_count: 464
- duration_s: 264.0
- tempo0: 120
- tempo_events: 1
- time_sig: 2/2
- max_poly: 1
- bar_density_mean: 3.515151515151515
- bar_density_p90: 5.0
- tracks: 1
- pitch_min: 56
- pitch_max: 77

## Conversion Snapshot
- top chord-zone usage: 0/427 (safe single-zone 427/427)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_strict
- reason: default guitar_literal_strict for maximal one-to-one feel

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
