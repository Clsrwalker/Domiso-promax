# Analysis (Guitar Literal Script): fur-elise-beethoven.mid

## Metrics
- note_count: 1040
- duration_s: 156.83901515151518
- tempo0: 72
- tempo_events: 2
- time_sig: 1/8
- max_poly: 6
- bar_density_mean: 2.7807486631016043
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 33
- pitch_max: 100

## Conversion Snapshot
- top chord-zone usage: 0/1049 (safe single-zone 1049/1049)
- chord pads injected: 0


## Recommended Profile
- guitar_literal_strict
- reason: default guitar_literal_strict for maximal one-to-one feel

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
