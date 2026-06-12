# Analysis (Guitar Literal Script): it-happened-quiet-aurora-piano-transcription.mid

## Metrics
- note_count: 1265
- duration_s: 244.4181818181818
- tempo0: 110
- tempo_events: 1
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 17.569444444444443
- bar_density_p90: 29.7
- tracks: 2
- pitch_min: 36
- pitch_max: 91

## Conversion Snapshot
- top chord-zone usage: 78/2121 (safe single-zone 2043/2121)
- chord pads injected: 53


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
