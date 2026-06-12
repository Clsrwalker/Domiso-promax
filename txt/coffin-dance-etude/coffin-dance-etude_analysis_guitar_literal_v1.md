# Analysis (Guitar Literal Script): coffin-dance-etude.mid

## Metrics
- note_count: 2230
- duration_s: 117.50086805555557
- tempo0: 144
- tempo_events: 1
- time_sig: 2/4
- max_poly: 5
- bar_density_mean: 15.815602836879433
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 22
- pitch_max: 103

## Conversion Snapshot
- top chord-zone usage: 12/1785 (safe single-zone 1773/1785)
- chord pads injected: 12


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
