# Analysis (Guitar Literal Script): 王国城堡1.mid

## Metrics
- note_count: 155
- duration_s: 41.620535714285715
- tempo0: 105
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 8.61111111111111
- bar_density_p90: 11.3
- tracks: 2
- pitch_min: 41
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 14/266 (safe single-zone 252/266)
- chord pads injected: 9


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
