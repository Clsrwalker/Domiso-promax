# Analysis (Guitar Literal Script): xin-ru-zhi-shui-ice-paper.mid

## Metrics
- note_count: 1466
- duration_s: 182.85714285714283
- tempo0: 126
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 15.270833333333334
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 44
- pitch_max: 82

## Conversion Snapshot
- top chord-zone usage: 34/1972 (safe single-zone 1938/1972)
- chord pads injected: 34


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
