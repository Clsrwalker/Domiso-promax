# Analysis (Guitar Literal Script): 春泥_-_庾澄庆（原版）.mid

## Metrics
- note_count: 3277
- duration_s: 252.61025641025643
- tempo0: 78
- tempo_events: 2
- time_sig: 4/4
- max_poly: 15
- bar_density_mean: 40.45679012345679
- bar_density_p90: 69.0
- tracks: 10
- pitch_min: 24
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 5/3968 (safe single-zone 3963/3968)
- chord pads injected: 5


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
