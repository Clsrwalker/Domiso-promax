# Analysis (Guitar Literal Script): xin-qiang-ren-jia-lun.mid

## Metrics
- note_count: 1515
- duration_s: 286.6666666666667
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 17.823529411764707
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 37
- pitch_max: 101

## Conversion Snapshot
- top chord-zone usage: 11/2068 (safe single-zone 2057/2068)
- chord pads injected: 11


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
