# Analysis (Guitar Literal Script): handclap-fitz-and-the-tantrums.mid

## Metrics
- note_count: 2586
- duration_s: 183.42857142857142
- tempo0: 140
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 24.16822429906542
- bar_density_p90: 34.0
- tracks: 2
- pitch_min: 31
- pitch_max: 96

## Conversion Snapshot
- top chord-zone usage: 21/2549 (safe single-zone 2528/2549)
- chord pads injected: 21


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
