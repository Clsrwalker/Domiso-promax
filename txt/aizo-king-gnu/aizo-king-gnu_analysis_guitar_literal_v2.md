# Analysis (Guitar Literal Script): aizo-king-gnu.mid

## Metrics
- note_count: 1237
- duration_s: 86.84210526315789
- tempo0: 190
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.92753623188406
- bar_density_p90: 25.0
- tracks: 2
- pitch_min: 33
- pitch_max: 100

## Conversion Snapshot
- top chord-zone usage: 48/1403 (safe single-zone 1355/1403)
- chord pads injected: 44


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
