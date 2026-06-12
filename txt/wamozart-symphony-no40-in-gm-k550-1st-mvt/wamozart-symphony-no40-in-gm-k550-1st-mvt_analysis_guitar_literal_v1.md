# Analysis (Guitar Literal Script): wamozart-symphony-no40-in-gm-k550-1st-mvt.mid

## Metrics
- note_count: 5533
- duration_s: 455.4
- tempo0: 210
- tempo_events: 1
- time_sig: 2/2
- max_poly: 7
- bar_density_mean: 13.867167919799499
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 36
- pitch_max: 91

## Conversion Snapshot
- top chord-zone usage: 155/6095 (safe single-zone 5940/6095)
- chord pads injected: 144


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
