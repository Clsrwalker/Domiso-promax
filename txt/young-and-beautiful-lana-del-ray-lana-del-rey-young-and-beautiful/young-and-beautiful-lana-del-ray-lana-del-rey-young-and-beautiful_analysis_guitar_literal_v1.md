# Analysis (Guitar Literal Script): young-and-beautiful-lana-del-ray-lana-del-rey-young-and-beautiful.mid

## Metrics
- note_count: 2073
- duration_s: 248.89004629629633
- tempo0: 108
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 18.508928571428573
- bar_density_p90: 27.0
- tracks: 2
- pitch_min: 26
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 20/2369 (safe single-zone 2349/2369)
- chord pads injected: 18


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
