# Analysis (Guitar Literal Script): detective-conan-main-theme.mid

## Metrics
- note_count: 2224
- duration_s: 184.87263858897362
- tempo0: 145
- tempo_events: 4
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 21.59223300970874
- bar_density_p90: 28.6
- tracks: 2
- pitch_min: 24
- pitch_max: 108

## Conversion Snapshot
- top chord-zone usage: 8/2286 (safe single-zone 2278/2286)
- chord pads injected: 8


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
