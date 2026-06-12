# Analysis (Guitar Literal Script): Come_Alive.mid

## Metrics
- note_count: 1309
- duration_s: 238.5590909090909
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 10.908333333333333
- bar_density_p90: 17.9
- tracks: 2
- pitch_min: 34
- pitch_max: 81

## Conversion Snapshot
- top chord-zone usage: 27/1407 (safe single-zone 1380/1407)
- chord pads injected: 25


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
