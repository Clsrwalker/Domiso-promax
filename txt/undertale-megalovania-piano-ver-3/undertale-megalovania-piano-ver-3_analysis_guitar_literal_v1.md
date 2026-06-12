# Analysis (Guitar Literal Script): undertale-megalovania-piano-ver-3.mid

## Metrics
- note_count: 1816
- duration_s: 155.99375
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.28205128205128
- bar_density_p90: 40.0
- tracks: 2
- pitch_min: 34
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 0/1635 (safe single-zone 1635/1635)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
