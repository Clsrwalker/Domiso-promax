# Analysis (Guitar Literal Script): ballade-pour-adeline-richard-clayderman.mid

## Metrics
- note_count: 912
- duration_s: 174.7543530772633
- tempo0: 60
- tempo_events: 11
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 21.209302325581394
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 0/1002 (safe single-zone 1002/1002)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
