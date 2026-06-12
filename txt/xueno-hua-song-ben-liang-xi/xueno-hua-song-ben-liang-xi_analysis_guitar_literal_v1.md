# Analysis (Guitar Literal Script): xueno-hua-song-ben-liang-xi.mid

## Metrics
- note_count: 1982
- duration_s: 193.525
- tempo0: 120
- tempo_events: 1
- time_sig: 1/4
- max_poly: 7
- bar_density_mean: 5.161458333333333
- bar_density_p90: 8.0
- tracks: 2
- pitch_min: 27
- pitch_max: 97

## Conversion Snapshot
- top chord-zone usage: 19/2433 (safe single-zone 2414/2433)
- chord pads injected: 18


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
