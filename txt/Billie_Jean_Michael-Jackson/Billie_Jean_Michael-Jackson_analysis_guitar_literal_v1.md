# Analysis (Guitar Literal Script): Billie_Jean_Michael Jackson.mid

## Metrics
- note_count: 2252
- duration_s: 255.20054347826084
- tempo0: 115
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.084745762711865
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 23
- pitch_max: 105

## Conversion Snapshot
- top chord-zone usage: 17/2276 (safe single-zone 2259/2276)
- chord pads injected: 17


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
