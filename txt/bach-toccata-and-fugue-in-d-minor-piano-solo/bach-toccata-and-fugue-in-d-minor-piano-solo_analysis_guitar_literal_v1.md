# Analysis (Guitar Literal Script): bach-toccata-and-fugue-in-d-minor-piano-solo.mid

## Metrics
- note_count: 4122
- duration_s: 439.1054577532607
- tempo0: 60
- tempo_events: 46
- time_sig: 4/4
- max_poly: 11
- bar_density_mean: 28.825174825174827
- bar_density_p90: 48.0
- tracks: 2
- pitch_min: 20
- pitch_max: 86

## Conversion Snapshot
- top chord-zone usage: 8/4403 (safe single-zone 4395/4403)
- chord pads injected: 8


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
