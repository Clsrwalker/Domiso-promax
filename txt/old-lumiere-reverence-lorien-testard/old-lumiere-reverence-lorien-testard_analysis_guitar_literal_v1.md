# Analysis (Guitar Literal Script): old-lumiere-reverence-lorien-testard.mid

## Metrics
- note_count: 1746
- duration_s: 249.84246575342468
- tempo0: 73
- tempo_events: 1
- time_sig: 2/4
- max_poly: 7
- bar_density_mean: 11.486842105263158
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 24
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 12/1816 (safe single-zone 1804/1816)
- chord pads injected: 11


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
