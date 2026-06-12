# Analysis (Guitar Literal Script): 王国城堡.mid

## Metrics
- note_count: 552
- duration_s: 135.6206191588785
- tempo0: 107
- tempo_events: 1
- time_sig: 4/4
- max_poly: 12
- bar_density_mean: 9.049180327868852
- bar_density_p90: 13.8
- tracks: 2
- pitch_min: 34
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 28/1011 (safe single-zone 983/1011)
- chord pads injected: 21


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
