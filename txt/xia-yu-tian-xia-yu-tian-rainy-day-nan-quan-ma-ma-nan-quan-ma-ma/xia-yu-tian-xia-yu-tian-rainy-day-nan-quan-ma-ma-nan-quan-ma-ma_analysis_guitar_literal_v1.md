# Analysis (Guitar Literal Script): xia-yu-tian-xia-yu-tian-rainy-day-nan-quan-ma-ma-nan-quan-ma-ma.mid

## Metrics
- note_count: 1178
- duration_s: 268.61538461538464
- tempo0: 65
- tempo_events: 1
- time_sig: 2/8
- max_poly: 7
- bar_density_mean: 4.090277777777778
- bar_density_p90: 6.0
- tracks: 2
- pitch_min: 32
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 8/1356 (safe single-zone 1348/1356)
- chord pads injected: 6


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
