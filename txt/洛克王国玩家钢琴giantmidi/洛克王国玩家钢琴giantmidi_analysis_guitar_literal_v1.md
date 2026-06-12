# Analysis (Guitar Literal Script): 洛克王国玩家钢琴giantmidi.mid

## Metrics
- note_count: 973
- duration_s: 178.11067708333334
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 18
- bar_density_mean: 11.447058823529412
- bar_density_p90: 18.0
- tracks: 1
- pitch_min: 34
- pitch_max: 103

## Conversion Snapshot
- top chord-zone usage: 48/1917 (safe single-zone 1869/1917)
- chord pads injected: 34


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
