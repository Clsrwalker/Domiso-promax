# Analysis (Guitar Literal Script): canon-in-d-violin-solo.mid

## Metrics
- note_count: 529
- duration_s: 218.57142857142856
- tempo0: 56
- tempo_events: 1
- time_sig: 4/4
- max_poly: 1
- bar_density_mean: 10.372549019607844
- bar_density_p90: 28.0
- tracks: 1
- pitch_min: 59
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 0/463 (safe single-zone 463/463)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
