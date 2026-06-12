# Analysis (Guitar Script): ff14诗人演奏樱花草.mid

## Metrics
- note_count: 493
- duration_s: 107.25903614457832
- tempo0: 83
- tempo_events: 1
- time_sig: 4/4
- max_poly: 2
- bar_density_mean: 13.324324324324325
- bar_density_p90: 15.2
- tracks: 1
- pitch_min: 48
- pitch_max: 81

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
- playability: 443/443 (100.00%)
- top chord-zone usage: 0/443 (safe 100.00%)
- chord pads injected: 0
- style windows: w00-w01:bass_strum, w02-w06:lead_mix, w07-w08:bass_strum, w09-w09:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 4, 'folk_strum': 0, 'lead_mix': 5, 'muted_strum': 0}
