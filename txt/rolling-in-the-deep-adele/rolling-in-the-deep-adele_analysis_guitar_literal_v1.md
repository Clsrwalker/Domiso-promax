# Analysis (Guitar Literal Script): rolling-in-the-deep-adele.mid

## Metrics
- note_count: 1007
- duration_s: 127.09499999999998
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.0
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 43
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 31/1187 (safe single-zone 1156/1187)
- chord pads injected: 30


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
