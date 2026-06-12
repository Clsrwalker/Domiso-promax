# Analysis (Guitar Literal Script): 青鸟 - 火影忍者.mid

## Metrics
- note_count: 1083
- duration_s: 88.0
- tempo0: 150
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 19.69090909090909
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 21
- pitch_max: 87

## Conversion Snapshot
- top chord-zone usage: 38/1303 (safe single-zone 1265/1303)
- chord pads injected: 37


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
