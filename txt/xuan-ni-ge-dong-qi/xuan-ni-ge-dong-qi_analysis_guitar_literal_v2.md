# Analysis (Guitar Literal Script): xuan-ni-ge-dong-qi.mid

## Metrics
- note_count: 1315
- duration_s: 200.59701492537314
- tempo0: 67
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.482142857142858
- bar_density_p90: 33.3
- tracks: 2
- pitch_min: 40
- pitch_max: 81

## Conversion Snapshot
- top chord-zone usage: 6/1285 (safe single-zone 1279/1285)
- chord pads injected: 5


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
