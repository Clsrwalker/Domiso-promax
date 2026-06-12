# Analysis (Guitar Literal Script): die-lian-die-lian.mid

## Metrics
- note_count: 1164
- duration_s: 212.50130208333334
- tempo0: 96
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.694117647058823
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 44
- pitch_max: 96

## Conversion Snapshot
- top chord-zone usage: 24/1420 (safe single-zone 1396/1420)
- chord pads injected: 24


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
