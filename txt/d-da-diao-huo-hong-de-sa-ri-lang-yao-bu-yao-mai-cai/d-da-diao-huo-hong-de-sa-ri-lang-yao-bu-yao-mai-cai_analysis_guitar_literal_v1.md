# Analysis (Guitar Literal Script): d-da-diao-huo-hong-de-sa-ri-lang-yao-bu-yao-mai-cai.mid

## Metrics
- note_count: 853
- duration_s: 117.5
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 14.457627118644067
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 42
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 32/928 (safe single-zone 896/928)
- chord pads injected: 32


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
