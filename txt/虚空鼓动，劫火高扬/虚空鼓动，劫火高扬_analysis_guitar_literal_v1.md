# Analysis (Guitar Literal Script): 虚空鼓动，劫火高扬.mid

## Metrics
- note_count: 1441
- duration_s: 193.97362442756955
- tempo0: 82
- tempo_events: 14
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 17.36144578313253
- bar_density_p90: 25.6
- tracks: 2
- pitch_min: 36
- pitch_max: 102

## Conversion Snapshot
- top chord-zone usage: 4/2028 (safe single-zone 2024/2028)
- chord pads injected: 3


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
