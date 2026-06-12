# Analysis (Guitar Literal Script): ennio-morricone-enduring-movement.mid

## Metrics
- note_count: 1681
- duration_s: 80.32575334821429
- tempo0: 168
- tempo_events: 3
- time_sig: 2/4
- max_poly: 7
- bar_density_mean: 15.144144144144144
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 21
- pitch_max: 99

## Conversion Snapshot
- top chord-zone usage: 0/1597 (safe single-zone 1597/1597)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
