# Analysis (Guitar Literal Script): NO_BATIDAO__ZXKAI.mid

## Metrics
- note_count: 973
- duration_s: 91.38461538461539
- tempo0: 130
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 19.857142857142858
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 34
- pitch_max: 89

## Conversion Snapshot
- top chord-zone usage: 2/797 (safe single-zone 795/797)
- chord pads injected: 2


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
