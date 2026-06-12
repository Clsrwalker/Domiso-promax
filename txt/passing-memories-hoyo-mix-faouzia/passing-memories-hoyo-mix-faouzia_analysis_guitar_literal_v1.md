# Analysis (Guitar Literal Script): passing-memories-hoyo-mix-faouzia.mid

## Metrics
- note_count: 1842
- duration_s: 206.15384615384613
- tempo0: 117
- tempo_events: 1
- time_sig: 12/8
- max_poly: 10
- bar_density_mean: 27.492537313432837
- bar_density_p90: 44.0
- tracks: 7
- pitch_min: 27
- pitch_max: 90

## Conversion Snapshot
- top chord-zone usage: 51/2335 (safe single-zone 2284/2335)
- chord pads injected: 43


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
