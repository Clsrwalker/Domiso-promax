# Analysis (Guitar Literal Script): squid-game-2-mingle-song-musique-du-carrousel-mastered.mid

## Metrics
- note_count: 1206
- duration_s: 97.81875000000001
- tempo0: 160
- tempo_events: 1
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 27.40909090909091
- bar_density_p90: 33.5
- tracks: 2
- pitch_min: 34
- pitch_max: 87

## Conversion Snapshot
- top chord-zone usage: 103/1455 (safe single-zone 1352/1455)
- chord pads injected: 58


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
