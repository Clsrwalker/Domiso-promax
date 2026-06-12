# Analysis (Guitar Literal Script): g-minor-bach.mid

## Metrics
- note_count: 1810
- duration_s: 158.28
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 27.424242424242426
- bar_density_p90: 34.0
- tracks: 3
- pitch_min: 34
- pitch_max: 80

## Conversion Snapshot
- top chord-zone usage: 1/1816 (safe single-zone 1815/1816)
- chord pads injected: 1


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
