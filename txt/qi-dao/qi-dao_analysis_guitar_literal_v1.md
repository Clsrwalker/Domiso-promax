# Analysis (Guitar Literal Script): qi-dao.mid

## Metrics
- note_count: 1028
- duration_s: 187.78509054478917
- tempo0: 76
- tempo_events: 4
- time_sig: 1/4
- max_poly: 6
- bar_density_mean: 4.3559322033898304
- bar_density_p90: 6.0
- tracks: 2
- pitch_min: 33
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 0/1208 (safe single-zone 1208/1208)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_strict
- reason: default guitar_literal_strict for maximal one-to-one feel

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
