# Analysis (Guitar Literal Script): xing-xing-zai-chang-ge-chun-yin-le-cmj.mid

## Metrics
- note_count: 1187
- duration_s: 176.66666666666669
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 22.826923076923077
- bar_density_p90: 35.8
- tracks: 2
- pitch_min: 41
- pitch_max: 101

## Conversion Snapshot
- top chord-zone usage: 1/1161 (safe single-zone 1160/1161)
- chord pads injected: 1


## Recommended Profile
- guitar_literal_dense
- reason: high polyphony/density -> guitar_literal_dense

## Guitar Literal Intent
- preserve source note density and rhythm as much as possible
- keep top row for chord triggers; avoid treating it as normal single-note row
- only apply unavoidable playable mapping (range fold + white-key snap + optional sparse chord pads)
