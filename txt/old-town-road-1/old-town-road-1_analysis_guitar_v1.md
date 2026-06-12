# Analysis (Guitar Script): old-town-road-1.mid

## Metrics
- note_count: 1105
- duration_s: 156.26086956521738
- tempo0: 69
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 25.113636363636363
- bar_density_p90: 37.0
- tracks: 2
- pitch_min: 38
- pitch_max: 85

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
- playability: 586/586 (100.00%)
- top chord-zone usage: 10/586 (safe 98.29%)
- chord pads injected: 10
- style windows: w00-w01:bass_strum, w02-w04:lead_mix, w05-w05:muted_strum, w06-w06:bass_strum, w07-w07:arpeggio, w08-w08:folk_strum, w09-w09:muted_strum, w10-w10:bass_strum, w11-w11:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 4, 'folk_strum': 1, 'lead_mix': 3, 'muted_strum': 2}
