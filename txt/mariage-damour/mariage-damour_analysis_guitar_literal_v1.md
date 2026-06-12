# Analysis (Guitar Literal Script): mariage-damour.mid

## Metrics
- note_count: 1631
- duration_s: 226.62895927601807
- tempo0: 90
- tempo_events: 4
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.188235294117646
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 26
- pitch_max: 110

## Conversion Snapshot
- top chord-zone usage: 5/1351 (safe single-zone 1346/1351)
- chord pads injected: 4


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
