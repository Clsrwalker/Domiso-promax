# Analysis (Guitar Script): jie-bu-diao.mid

## Metrics
- note_count: 576
- duration_s: 180.0
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 10.666666666666666
- bar_density_p90: 17.0
- tracks: 2
- pitch_min: 36
- pitch_max: 88

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
- playability: 504/504 (100.00%)
- top chord-zone usage: 28/504 (safe 94.44%)
- chord pads injected: 28
- style windows: w00-w00:bass_strum, w01-w01:arpeggio, w02-w02:folk_strum, w03-w06:lead_mix, w07-w08:bass_strum, w09-w10:lead_mix, w11-w11:bass_strum, w12-w13:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 4, 'folk_strum': 1, 'lead_mix': 6, 'muted_strum': 0}
