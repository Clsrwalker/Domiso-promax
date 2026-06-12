# Analysis (Guitar Literal Script): 雨爱.mid

## Metrics
- note_count: 1056
- duration_s: 258.6782762691854
- tempo0: 154
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 6.36144578313253
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 35
- pitch_max: 85

## Conversion Snapshot
- top chord-zone usage: 119/1436 (safe single-zone 1317/1436)
- chord pads injected: 114


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
