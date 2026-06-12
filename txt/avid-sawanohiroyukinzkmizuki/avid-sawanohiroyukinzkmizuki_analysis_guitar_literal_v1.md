# Analysis (Guitar Literal Script): avid-sawanohiroyukinzkmizuki.mid

## Metrics
- note_count: 2468
- duration_s: 185.57115384615386
- tempo0: 120
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 26.82608695652174
- bar_density_p90: 40.0
- tracks: 2
- pitch_min: 33
- pitch_max: 103

## Conversion Snapshot
- top chord-zone usage: 0/2930 (safe single-zone 2930/2930)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
