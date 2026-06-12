# Analysis (Guitar Literal Script): kamado-tanjiro-no-uta (1).mid

## Metrics
- note_count: 646
- duration_s: 74.87583333333333
- tempo0: 150
- tempo_events: 3
- time_sig: 1/4
- max_poly: 8
- bar_density_mean: 3.530054644808743
- bar_density_p90: 6.0
- tracks: 2
- pitch_min: 29
- pitch_max: 98

## Conversion Snapshot
- top chord-zone usage: 55/862 (safe single-zone 807/862)
- chord pads injected: 45


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
