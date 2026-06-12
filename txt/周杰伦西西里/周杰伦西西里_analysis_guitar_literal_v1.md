# Analysis (Guitar Literal Script): 周杰伦西西里.mid

## Metrics
- note_count: 1354
- duration_s: 226.7599587912088
- tempo0: 91
- tempo_events: 1
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 15.744186046511627
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 36
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 1/1638 (safe single-zone 1637/1638)
- chord pads injected: 1


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
