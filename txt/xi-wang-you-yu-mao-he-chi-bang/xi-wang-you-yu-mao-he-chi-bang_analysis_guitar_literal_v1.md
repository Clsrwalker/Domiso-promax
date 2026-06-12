# Analysis (Guitar Literal Script): xi-wang-you-yu-mao-he-chi-bang.mid

## Metrics
- note_count: 2284
- duration_s: 240.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.033333333333335
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 37
- pitch_max: 100

## Conversion Snapshot
- top chord-zone usage: 26/2721 (safe single-zone 2695/2721)
- chord pads injected: 25


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
