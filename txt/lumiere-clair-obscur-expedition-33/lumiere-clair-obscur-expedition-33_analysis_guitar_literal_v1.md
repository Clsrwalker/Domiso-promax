# Analysis (Guitar Literal Script): lumiere-clair-obscur-expedition-33.mid

## Metrics
- note_count: 1496
- duration_s: 220.59163568816507
- tempo0: 82
- tempo_events: 6
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.946666666666665
- bar_density_p90: 30.0
- tracks: 2
- pitch_min: 31
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 20/1673 (safe single-zone 1653/1673)
- chord pads injected: 18


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
