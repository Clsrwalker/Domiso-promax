# Analysis (Guitar Literal Script): mission-impossible-theme-lalo-schifrin.mid

## Metrics
- note_count: 2756
- duration_s: 193.805
- tempo0: 100
- tempo_events: 3
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 25.51851851851852
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 26
- pitch_max: 108

## Conversion Snapshot
- top chord-zone usage: 2/2684 (safe single-zone 2682/2684)
- chord pads injected: 1


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
