# Analysis (Guitar Literal Script): 12-variations-of-twinkle-twinkle-little-star.mid

## Metrics
- note_count: 6294
- duration_s: 687.475
- tempo0: 120
- tempo_events: 3
- time_sig: 2/4
- max_poly: 8
- bar_density_mean: 9.478915662650602
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 29
- pitch_max: 89

## Conversion Snapshot
- top chord-zone usage: 73/7643 (safe single-zone 7570/7643)
- chord pads injected: 73


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
