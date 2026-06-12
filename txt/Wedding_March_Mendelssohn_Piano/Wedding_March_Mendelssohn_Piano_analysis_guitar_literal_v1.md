# Analysis (Guitar Literal Script): Wedding_March_Mendelssohn_Piano.mid

## Metrics
- note_count: 4617
- duration_s: 294.64000000000004
- tempo0: 150
- tempo_events: 1
- time_sig: 1/4
- max_poly: 7
- bar_density_mean: 6.324657534246575
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 26
- pitch_max: 88

## Conversion Snapshot
- top chord-zone usage: 94/4136 (safe single-zone 4042/4136)
- chord pads injected: 84


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
