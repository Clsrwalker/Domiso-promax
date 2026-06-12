# Analysis (Guitar Literal Script): from-the-start-laufey.mid

## Metrics
- note_count: 1458
- duration_s: 178.54333150473406
- tempo0: 164
- tempo_events: 6
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 13.626168224299066
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 39
- pitch_max: 89

## Conversion Snapshot
- top chord-zone usage: 78/1990 (safe single-zone 1912/1990)
- chord pads injected: 73


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
