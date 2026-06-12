# Analysis (Guitar Literal Script): sonate-no-14-moonlight-3rd-movement.mid

## Metrics
- note_count: 6552
- duration_s: 404.35083502253894
- tempo0: 164
- tempo_events: 19
- time_sig: 4/4
- max_poly: 12
- bar_density_mean: 24.44776119402985
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 29
- pitch_max: 88

## Conversion Snapshot
- top chord-zone usage: 13/7096 (safe single-zone 7083/7096)
- chord pads injected: 10


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
