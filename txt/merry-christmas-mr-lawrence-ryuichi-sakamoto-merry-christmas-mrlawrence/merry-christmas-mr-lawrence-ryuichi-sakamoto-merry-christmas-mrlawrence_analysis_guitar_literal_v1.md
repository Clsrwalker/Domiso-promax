# Analysis (Guitar Literal Script): merry-christmas-mr-lawrence-ryuichi-sakamoto-merry-christmas-mrlawrence.mid

## Metrics
- note_count: 3039
- duration_s: 289.4417582417582
- tempo0: 104
- tempo_events: 3
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 19.11320754716981
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 29
- pitch_max: 97

## Conversion Snapshot
- top chord-zone usage: 80/3059 (safe single-zone 2979/3059)
- chord pads injected: 47


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
