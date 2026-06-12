# Analysis (Guitar Literal Script): fantaisie-impromptu-in-c-minor-chopin.mid

## Metrics
- note_count: 3049
- duration_s: 327.51022460328124
- tempo0: 168
- tempo_events: 38
- time_sig: 2/2
- max_poly: 6
- bar_density_mean: 22.094202898550726
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 100

## Conversion Snapshot
- top chord-zone usage: 1/3132 (safe single-zone 3131/3132)
- chord pads injected: 1


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
