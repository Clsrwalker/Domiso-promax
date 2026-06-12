# Analysis (Guitar Literal Script): the-first-take-kataomoi-aimer-aimer-kataomoi-the-first-take-piano.mid

## Metrics
- note_count: 1282
- duration_s: 205.36082474226805
- tempo0: 97
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 15.44578313253012
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 30
- pitch_max: 97

## Conversion Snapshot
- top chord-zone usage: 47/1527 (safe single-zone 1480/1527)
- chord pads injected: 34


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
