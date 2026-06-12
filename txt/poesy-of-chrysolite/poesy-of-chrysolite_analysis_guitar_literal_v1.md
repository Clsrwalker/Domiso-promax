# Analysis (Guitar Literal Script): poesy-of-chrysolite.mid

## Metrics
- note_count: 1163
- duration_s: 139.41195568280182
- tempo0: 94
- tempo_events: 11
- time_sig: 1/8
- max_poly: 7
- bar_density_mean: 2.60762331838565
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 31
- pitch_max: 91

## Conversion Snapshot
- top chord-zone usage: 23/1445 (safe single-zone 1422/1445)
- chord pads injected: 23


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
