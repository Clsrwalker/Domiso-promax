# Analysis (Guitar Literal Script): 4-variations-on-happy-birthday.mid

## Metrics
- note_count: 1031
- duration_s: 83.08757763975156
- tempo0: 150
- tempo_events: 4
- time_sig: 3/4
- max_poly: 7
- bar_density_mean: 14.728571428571428
- bar_density_p90: 23.9
- tracks: 2
- pitch_min: 38
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 19/1152 (safe single-zone 1133/1152)
- chord pads injected: 19


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
