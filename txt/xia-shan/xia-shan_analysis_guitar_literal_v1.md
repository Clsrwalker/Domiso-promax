# Analysis (Guitar Literal Script): xia-shan.mid

## Metrics
- note_count: 1411
- duration_s: 169.609756097561
- tempo0: 82
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 24.32758620689655
- bar_density_p90: 31.0
- tracks: 2
- pitch_min: 32
- pitch_max: 90

## Conversion Snapshot
- top chord-zone usage: 5/1447 (safe single-zone 1442/1447)
- chord pads injected: 4


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
