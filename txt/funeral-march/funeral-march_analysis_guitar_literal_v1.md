# Analysis (Guitar Literal Script): funeral-march.mid

## Metrics
- note_count: 2106
- duration_s: 539.875
- tempo0: 48
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 19.5
- bar_density_p90: 31.0
- tracks: 2
- pitch_min: 25
- pitch_max: 89

## Conversion Snapshot
- top chord-zone usage: 62/2364 (safe single-zone 2302/2364)
- chord pads injected: 61


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
