# Analysis (Guitar Literal Script): 山中好长日_音乐OST_逢归的谶羽.mid

## Metrics
- note_count: 1074
- duration_s: 240.82066441441444
- tempo0: 111
- tempo_events: 1
- time_sig: 4/4
- max_poly: 10
- bar_density_mean: 9.675675675675675
- bar_density_p90: 13.0
- tracks: 2
- pitch_min: 42
- pitch_max: 102

## Conversion Snapshot
- top chord-zone usage: 24/1955 (safe single-zone 1931/1955)
- chord pads injected: 17


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
