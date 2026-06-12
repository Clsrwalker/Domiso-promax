# Analysis (Guitar Literal Script): genshin_蒙德荆夫港.mid

## Metrics
- note_count: 924
- duration_s: 277.56612318840575
- tempo0: 69
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 20.533333333333335
- bar_density_p90: 28.4
- tracks: 2
- pitch_min: 33
- pitch_max: 95

## Conversion Snapshot
- top chord-zone usage: 6/891 (safe single-zone 885/891)
- chord pads injected: 4


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
