# Analysis (Guitar Literal Script): 如生之不竭.mid

## Metrics
- note_count: 1562
- duration_s: 151.69811320754715
- tempo0: 106
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 23.313432835820894
- bar_density_p90: 33.4
- tracks: 2
- pitch_min: 38
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 6/1599 (safe single-zone 1593/1599)
- chord pads injected: 6


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
