# Analysis (Guitar Literal Script): 洛克王国彼得大道、人鱼湾.mid

## Metrics
- note_count: 446
- duration_s: 33.229166666666664
- tempo0: 132
- tempo_events: 1
- time_sig: 4/4
- max_poly: 19
- bar_density_mean: 23.473684210526315
- bar_density_p90: 41.0
- tracks: 1
- pitch_min: 36
- pitch_max: 106

## Conversion Snapshot
- top chord-zone usage: 7/747 (safe single-zone 740/747)
- chord pads injected: 6


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
