# Analysis (Guitar Literal Script): Assassin_Creed_ezios-family.mid

## Metrics
- note_count: 761
- duration_s: 130.67364718614718
- tempo0: 140
- tempo_events: 5
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 10.146666666666667
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 31
- pitch_max: 91

## Conversion Snapshot
- top chord-zone usage: 30/954 (safe single-zone 924/954)
- chord pads injected: 28


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
