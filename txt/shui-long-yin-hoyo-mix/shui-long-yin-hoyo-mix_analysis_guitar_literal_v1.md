# Analysis (Guitar Literal Script): shui-long-yin-hoyo-mix.mid

## Metrics
- note_count: 851
- duration_s: 171.06382978723406
- tempo0: 47
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 25.78787878787879
- bar_density_p90: 40.6
- tracks: 2
- pitch_min: 28
- pitch_max: 85

## Conversion Snapshot
- top chord-zone usage: 10/960 (safe single-zone 950/960)
- chord pads injected: 8


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
