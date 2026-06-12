# Analysis (Guitar Literal Script): 月光的赞美诗_乘月亮船上月球背景音乐.mid

## Metrics
- note_count: 1054
- duration_s: 193.29427083333334
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 11.094736842105263
- bar_density_p90: 17.0
- tracks: 2
- pitch_min: 34
- pitch_max: 101

## Conversion Snapshot
- top chord-zone usage: 57/1574 (safe single-zone 1517/1574)
- chord pads injected: 43


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
