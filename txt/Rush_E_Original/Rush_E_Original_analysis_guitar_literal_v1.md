# Analysis (Guitar Literal Script): Rush_E_Original.mid

## Metrics
- note_count: 19232
- duration_s: 271.95
- tempo0: 300
- tempo_events: 1
- time_sig: 4/4
- max_poly: 123
- bar_density_mean: 57.23809523809524
- bar_density_p90: 248.6
- tracks: 3
- pitch_min: 24
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 236/13245 (safe single-zone 13009/13245)
- chord pads injected: 195


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
