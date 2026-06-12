# Analysis (Guitar Literal Script): happy-birthday-variations.mid

## Metrics
- note_count: 2588
- duration_s: 320.7031096354626
- tempo0: 65
- tempo_events: 21
- time_sig: 1/4
- max_poly: 9
- bar_density_mean: 4.1877022653721685
- bar_density_p90: 7.0
- tracks: 2
- pitch_min: 25
- pitch_max: 100

## Conversion Snapshot
- top chord-zone usage: 60/2826 (safe single-zone 2766/2826)
- chord pads injected: 51


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
