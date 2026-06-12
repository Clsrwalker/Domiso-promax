# Analysis (Guitar Literal Script): guang-hui-sui-yue.mid

## Metrics
- note_count: 1707
- duration_s: 186.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 18.35483870967742
- bar_density_p90: 27.0
- tracks: 2
- pitch_min: 28
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 34/1858 (safe single-zone 1824/1858)
- chord pads injected: 34


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
