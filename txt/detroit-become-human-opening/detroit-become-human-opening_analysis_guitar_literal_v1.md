# Analysis (Guitar Literal Script): detroit-become-human-opening.mid

## Metrics
- note_count: 586
- duration_s: 100.00208333333333
- tempo0: 60
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.44
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 36
- pitch_max: 88

## Conversion Snapshot
- top chord-zone usage: 0/761 (safe single-zone 761/761)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
