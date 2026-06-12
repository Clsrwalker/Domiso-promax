# Analysis (Guitar Literal Script): Animenz王者荣耀.mid

## Metrics
- note_count: 5301
- duration_s: 506.0611979166667
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 23
- bar_density_mean: 21.204
- bar_density_p90: 32.0
- tracks: 1
- pitch_min: 26
- pitch_max: 104

## Conversion Snapshot
- top chord-zone usage: 37/8199 (safe single-zone 8162/8199)
- chord pads injected: 25


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
