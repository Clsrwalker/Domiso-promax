# Analysis (Guitar Literal Script): to-the-end-of-all-wars.mid

## Metrics
- note_count: 2910
- duration_s: 208.66071428571428
- tempo0: 112
- tempo_events: 1
- time_sig: 1/4
- max_poly: 12
- bar_density_mean: 7.461538461538462
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 21
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 2/3722 (safe single-zone 3720/3722)
- chord pads injected: 2


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
