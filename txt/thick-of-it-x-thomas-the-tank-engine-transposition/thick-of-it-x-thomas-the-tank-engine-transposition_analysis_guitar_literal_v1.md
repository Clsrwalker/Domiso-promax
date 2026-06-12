# Analysis (Guitar Literal Script): thick-of-it-x-thomas-the-tank-engine-transposition.mid

## Metrics
- note_count: 766
- duration_s: 57.33333333333333
- tempo0: 180
- tempo_events: 1
- time_sig: 2/2
- max_poly: 6
- bar_density_mean: 18.238095238095237
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 28
- pitch_max: 85

## Conversion Snapshot
- top chord-zone usage: 46/931 (safe single-zone 885/931)
- chord pads injected: 41


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
