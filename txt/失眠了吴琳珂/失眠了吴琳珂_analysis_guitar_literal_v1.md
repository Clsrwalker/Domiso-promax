# Analysis (Guitar Literal Script): 失眠了吴琳珂.mid

## Metrics
- note_count: 895
- duration_s: 251.99213286713285
- tempo0: 104
- tempo_events: 1
- time_sig: 4/4
- max_poly: 10
- bar_density_mean: 8.211009174311927
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 36
- pitch_max: 82

## Conversion Snapshot
- top chord-zone usage: 54/2017 (safe single-zone 1963/2017)
- chord pads injected: 41


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
