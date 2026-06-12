# Analysis (Guitar Literal Script): ni-de-bei-bao.mid

## Metrics
- note_count: 1325
- duration_s: 205.53214285714284
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 22.45762711864407
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 25
- pitch_max: 88

## Conversion Snapshot
- top chord-zone usage: 0/1507 (safe single-zone 1507/1507)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
