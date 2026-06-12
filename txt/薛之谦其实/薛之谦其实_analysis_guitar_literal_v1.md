# Analysis (Guitar Literal Script): 薛之谦其实.mid

## Metrics
- note_count: 906
- duration_s: 238.679806918745
- tempo0: 113
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 8.089285714285714
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 32
- pitch_max: 85

## Conversion Snapshot
- top chord-zone usage: 42/1578 (safe single-zone 1536/1578)
- chord pads injected: 33


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
