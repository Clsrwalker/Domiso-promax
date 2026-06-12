# Analysis (Guitar Literal Script): 星穹铁道耀斑.mid

## Metrics
- note_count: 1778
- duration_s: 220.9018181818182
- tempo0: 150
- tempo_events: 1
- time_sig: 4/4
- max_poly: 13
- bar_density_mean: 12.884057971014492
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 31
- pitch_max: 88

## Conversion Snapshot
- top chord-zone usage: 37/1920 (safe single-zone 1883/1920)
- chord pads injected: 27


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
