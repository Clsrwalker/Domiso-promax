# Analysis (Guitar Literal Script): 爱琴海周杰伦.mid

## Metrics
- note_count: 1049
- duration_s: 215.5407754010695
- tempo0: 136
- tempo_events: 1
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 8.528455284552846
- bar_density_p90: 13.0
- tracks: 2
- pitch_min: 38
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 54/1300 (safe single-zone 1246/1300)
- chord pads injected: 49


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
