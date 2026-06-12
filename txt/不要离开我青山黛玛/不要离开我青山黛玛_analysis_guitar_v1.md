# Analysis (Guitar Script): 不要离开我青山黛玛.mid

## Metrics
- note_count: 1129
- duration_s: 232.7455357142857
- tempo0: 91
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 12.685393258426966
- bar_density_p90: 17.0
- tracks: 2
- pitch_min: 39
- pitch_max: 91

## Recommended Profile
- guitar_dense
- reason: high density/polyphony -> guitar dense profile with anti-mud limits

## Guitar Script Intent
- melody mapping avoids direct top-row chord-trigger substitution
- accompaniment may trigger top-row chord keys from bass anchors (controlled density)
- keep key layout compatible with normal DoMiSo positions
- optimize arrangement for guitar timbre by reducing muddy overlap
- keep melody clear while simplifying accompaniment density
- maintain 21-key playability and parser-safe syntax


## Output Checks
- playability: 590/590 (100.00%)
- top chord-zone usage: 53/590 (safe 91.02%)
- chord pads injected: 53
- style windows: w00-w01:arpeggio, w02-w02:folk_strum, w03-w06:bass_strum, w07-w08:folk_strum, w09-w11:bass_strum, w12-w14:muted_strum, w15-w17:folk_strum, w18-w20:lead_mix, w21-w21:folk_strum, w22-w22:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 7, 'folk_strum': 7, 'lead_mix': 3, 'muted_strum': 3}
