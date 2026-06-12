# Analysis (Guitar Literal Script): flower-dance-dj-okawari.mid

## Metrics
- note_count: 2332
- duration_s: 270.0657871540225
- tempo0: 80
- tempo_events: 12
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 22.20952380952381
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 31
- pitch_max: 104

## Conversion Snapshot
- top chord-zone usage: 4/2318 (safe single-zone 2314/2318)
- chord pads injected: 4


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
