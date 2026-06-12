# Analysis (Guitar Literal Script): sis-puella-magica-puella-magi-madoka-magica-yuki-kajiura.mid

## Metrics
- note_count: 1386
- duration_s: 189.5
- tempo0: 120
- tempo_events: 1
- time_sig: 3/4
- max_poly: 9
- bar_density_mean: 11.0
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 27
- pitch_max: 87

## Conversion Snapshot
- top chord-zone usage: 65/1771 (safe single-zone 1706/1771)
- chord pads injected: 57


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
