# Analysis (Guitar Literal Script): 终末地主题曲Give_Me_Something.mid

## Metrics
- note_count: 835
- duration_s: 159.255980861244
- tempo0: 114
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 10.986842105263158
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 32
- pitch_max: 82

## Conversion Snapshot
- top chord-zone usage: 8/1026 (safe single-zone 1018/1026)
- chord pads injected: 8


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
