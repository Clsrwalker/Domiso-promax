# Analysis (Guitar Literal Script): Billie_Jean.mid

## Metrics
- note_count: 5972
- duration_s: 294.91525423728814
- tempo0: 118
- tempo_events: 1
- time_sig: 4/4
- max_poly: 13
- bar_density_mean: 41.186206896551724
- bar_density_p90: 50.0
- tracks: 9
- pitch_min: 30
- pitch_max: 85

## Conversion Snapshot
- top chord-zone usage: 1/4758 (safe single-zone 4757/4758)
- chord pads injected: 1


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
