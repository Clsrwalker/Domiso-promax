# Analysis (Guitar Literal Script): mei-li-de-shen-hua.mid

## Metrics
- note_count: 1820
- duration_s: 314.0
- tempo0: 60
- tempo_events: 2
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 23.636363636363637
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 29
- pitch_max: 94

## Conversion Snapshot
- top chord-zone usage: 12/2200 (safe single-zone 2188/2200)
- chord pads injected: 11


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
