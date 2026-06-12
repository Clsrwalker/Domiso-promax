# Analysis (Guitar Literal Script): 将世事高枕.mid

## Metrics
- note_count: 679
- duration_s: 133.84855769230768
- tempo0: 104
- tempo_events: 2
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 11.912280701754385
- bar_density_p90: 17.4
- tracks: 2
- pitch_min: 37
- pitch_max: 87

## Conversion Snapshot
- top chord-zone usage: 9/1118 (safe single-zone 1109/1118)
- chord pads injected: 9


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
