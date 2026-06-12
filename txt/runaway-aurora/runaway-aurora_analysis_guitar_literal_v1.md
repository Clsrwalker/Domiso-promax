# Analysis (Guitar Literal Script): runaway-aurora.mid

## Metrics
- note_count: 1802
- duration_s: 323.90643236074277
- tempo0: 58
- tempo_events: 2
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 15.669565217391304
- bar_density_p90: 26.8
- tracks: 2
- pitch_min: 28
- pitch_max: 99

## Conversion Snapshot
- top chord-zone usage: 29/2316 (safe single-zone 2287/2316)
- chord pads injected: 21


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
