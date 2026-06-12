# Analysis (Guitar Literal Script): horizon-janji.mid

## Metrics
- note_count: 1984
- duration_s: 187.5009765625
- tempo0: 128
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.84
- bar_density_p90: 41.0
- tracks: 2
- pitch_min: 42
- pitch_max: 92

## Conversion Snapshot
- top chord-zone usage: 30/2007 (safe single-zone 1977/2007)
- chord pads injected: 21


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
