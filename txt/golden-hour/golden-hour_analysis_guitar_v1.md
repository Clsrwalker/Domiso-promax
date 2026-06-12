# Analysis (Guitar Script): golden-hour.mid

## Metrics
- note_count: 1073
- duration_s: 90.0
- tempo0: 96
- tempo_events: 1
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 44.708333333333336
- bar_density_p90: 59.0
- tracks: 2
- pitch_min: 40
- pitch_max: 92

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
- playability: 422/422 (100.00%)
- top chord-zone usage: 0/422 (safe 100.00%)
- chord pads injected: 0
- style windows: w00-w01:lead_mix, w02-w03:folk_strum, w04-w04:bass_strum, w05-w06:lead_mix, w07-w08:bass_strum, w09-w09:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 3, 'folk_strum': 2, 'lead_mix': 4, 'muted_strum': 0}
