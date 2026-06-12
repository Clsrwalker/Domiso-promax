# Analysis (Guitar Literal Script): shi-nian-chen-yi-xun.mid

## Metrics
- note_count: 1751
- duration_s: 199.35483870967744
- tempo0: 124
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.166666666666668
- bar_density_p90: 25.7
- tracks: 2
- pitch_min: 27
- pitch_max: 89

## Conversion Snapshot
- top chord-zone usage: 7/1968 (safe single-zone 1961/1968)
- chord pads injected: 5


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
