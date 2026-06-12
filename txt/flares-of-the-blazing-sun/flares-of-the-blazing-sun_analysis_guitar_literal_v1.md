# Analysis (Guitar Literal Script): flares-of-the-blazing-sun.mid

## Metrics
- note_count: 2713
- duration_s: 194.39872270896524
- tempo0: 148
- tempo_events: 4
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 23.188034188034187
- bar_density_p90: 34.2
- tracks: 2
- pitch_min: 21
- pitch_max: 105

## Conversion Snapshot
- top chord-zone usage: 43/2777 (safe single-zone 2734/2777)
- chord pads injected: 39


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
