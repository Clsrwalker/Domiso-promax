# Analysis (Guitar Literal Script): cheng-dou-misc-traditional.mid

## Metrics
- note_count: 1903
- duration_s: 271.9
- tempo0: 90
- tempo_events: 1
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 13.992647058823529
- bar_density_p90: 17.0
- tracks: 3
- pitch_min: 38
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 31/2210 (safe single-zone 2179/2210)
- chord pads injected: 20


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
