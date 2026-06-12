# Analysis (Guitar Script): shock-tv-ver.mid

## Metrics
- note_count: 329
- duration_s: 83.48007246376811
- tempo0: 69
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 13.708333333333334
- bar_density_p90: 18.0
- tracks: 2
- pitch_min: 40
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
- playability: 258/258 (100.00%)
- top chord-zone usage: 4/258 (safe 98.45%)
- chord pads injected: 4
- style windows: w00-w00:folk_strum, w01-w01:bass_strum, w02-w03:lead_mix, w04-w04:muted_strum, w05-w05:bass_strum, w06-w06:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 2, 'folk_strum': 1, 'lead_mix': 2, 'muted_strum': 1}
