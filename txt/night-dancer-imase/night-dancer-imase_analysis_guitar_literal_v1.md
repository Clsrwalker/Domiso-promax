# Analysis (Guitar Literal Script): night-dancer-imase.mid

## Metrics
- note_count: 1787
- duration_s: 210.0547201448854
- tempo0: 117
- tempo_events: 5
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.693069306930692
- bar_density_p90: 24.8
- tracks: 2
- pitch_min: 29
- pitch_max: 89

## Conversion Snapshot
- top chord-zone usage: 31/1973 (safe single-zone 1942/1973)
- chord pads injected: 25


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
