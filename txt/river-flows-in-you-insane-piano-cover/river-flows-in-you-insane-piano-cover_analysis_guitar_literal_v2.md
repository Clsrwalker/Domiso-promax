# Analysis (Guitar Literal Script): river-flows-in-you-insane-piano-cover.mid

## Metrics
- note_count: 1209
- duration_s: 199.10904720279717
- tempo0: 55
- tempo_events: 12
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 25.1875
- bar_density_p90: 49.7
- tracks: 2
- pitch_min: 26
- pitch_max: 93

## Conversion Snapshot
- top chord-zone usage: 3/1315 (safe single-zone 1312/1315)
- chord pads injected: 3


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
