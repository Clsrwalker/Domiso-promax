# Analysis (Guitar Literal Script): imagine-dragons-bones.mid

## Metrics
- note_count: 1749
- duration_s: 158.94627192982458
- tempo0: 57
- tempo_events: 3
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 23.635135135135137
- bar_density_p90: 35.0
- tracks: 2
- pitch_min: 22
- pitch_max: 89

## Conversion Snapshot
- top chord-zone usage: 12/1818 (safe single-zone 1806/1818)
- chord pads injected: 12


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
