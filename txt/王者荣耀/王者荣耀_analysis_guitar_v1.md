# Analysis (Guitar Script): 王者荣耀.mid

## Metrics
- note_count: 245
- duration_s: 72.314453125
- tempo0: 96
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 11.136363636363637
- bar_density_p90: 15.7
- tracks: 2
- pitch_min: 31
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
- playability: 199/199 (100.00%)
- top chord-zone usage: 19/199 (safe 90.45%)
- chord pads injected: 19
- style windows: w00-w00:bass_strum, w01-w01:arpeggio, w02-w02:lead_mix, w03-w03:muted_strum, w04-w05:bass_strum
- style counts: {'arpeggio': 1, 'bass_strum': 3, 'folk_strum': 0, 'lead_mix': 1, 'muted_strum': 1}
