# Analysis (Guitar Literal Script): jiu-wan-zi.mid

## Metrics
- note_count: 1155
- duration_s: 219.6923076923077
- tempo0: 65
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.576271186440678
- bar_density_p90: 30.0
- tracks: 2
- pitch_min: 27
- pitch_max: 92

## Conversion Snapshot
- top chord-zone usage: 2/1446 (safe single-zone 1444/1446)
- chord pads injected: 2


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
