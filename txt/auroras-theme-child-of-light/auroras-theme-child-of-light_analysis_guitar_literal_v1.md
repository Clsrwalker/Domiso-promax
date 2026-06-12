# Analysis (Guitar Literal Script): auroras-theme-child-of-light.mid

## Metrics
- note_count: 933
- duration_s: 162.78846153846155
- tempo0: 65
- tempo_events: 2
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.4375
- bar_density_p90: 29.1
- tracks: 2
- pitch_min: 36
- pitch_max: 103

## Conversion Snapshot
- top chord-zone usage: 5/781 (safe single-zone 776/781)
- chord pads injected: 5


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
