# Analysis (Guitar Literal Script): su-reverse-corsak.mid

## Metrics
- note_count: 1778
- duration_s: 239.99821428571428
- tempo0: 70
- tempo_events: 3
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 25.768115942028984
- bar_density_p90: 44.0
- tracks: 2
- pitch_min: 27
- pitch_max: 85

## Conversion Snapshot
- top chord-zone usage: 4/1684 (safe single-zone 1680/1684)
- chord pads injected: 3


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
