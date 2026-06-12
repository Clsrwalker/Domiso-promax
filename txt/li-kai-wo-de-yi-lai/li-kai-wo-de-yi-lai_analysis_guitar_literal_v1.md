# Analysis (Guitar Literal Script): li-kai-wo-de-yi-lai.mid

## Metrics
- note_count: 1176
- duration_s: 221.53846153846155
- tempo0: 65
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.6
- bar_density_p90: 30.0
- tracks: 2
- pitch_min: 34
- pitch_max: 94

## Conversion Snapshot
- top chord-zone usage: 11/1372 (safe single-zone 1361/1372)
- chord pads injected: 9


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
