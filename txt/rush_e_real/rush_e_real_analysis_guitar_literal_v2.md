# Analysis (Guitar Literal Script): rush_e_real.mid

## Metrics
- note_count: 46291
- duration_s: 141.2309105390356
- tempo0: 120
- tempo_events: 103
- time_sig: 4/4
- max_poly: 164
- bar_density_mean: 585.9620253164557
- bar_density_p90: 1096.0
- tracks: 12
- pitch_min: 0
- pitch_max: 127

## Conversion Snapshot
- top chord-zone usage: 13/5662 (safe single-zone 5649/5662)
- chord pads injected: 13


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
