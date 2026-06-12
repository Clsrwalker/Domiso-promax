# Analysis (Guitar Literal Script): take-me-hand.mid

## Metrics
- note_count: 1477
- duration_s: 258.64453125
- tempo0: 128
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 10.781021897810218
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 43
- pitch_max: 81

## Conversion Snapshot
- top chord-zone usage: 0/1927 (safe single-zone 1927/1927)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_strict
- reason: default guitar_literal_strict for maximal one-to-one feel

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
