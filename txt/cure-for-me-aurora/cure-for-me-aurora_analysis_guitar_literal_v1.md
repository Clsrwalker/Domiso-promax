# Analysis (Guitar Literal Script): cure-for-me-aurora.mid

## Metrics
- note_count: 2441
- duration_s: 189.85
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 25.694736842105264
- bar_density_p90: 43.4
- tracks: 2
- pitch_min: 25
- pitch_max: 97

## Conversion Snapshot
- top chord-zone usage: 21/2912 (safe single-zone 2891/2912)
- chord pads injected: 17


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
