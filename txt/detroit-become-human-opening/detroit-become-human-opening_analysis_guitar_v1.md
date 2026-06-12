# Analysis (Guitar Script): detroit-become-human-opening.mid

## Metrics
- note_count: 586
- duration_s: 100.00208333333333
- tempo0: 60
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 23.44
- bar_density_p90: 32.0
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
- playability: 168/168 (100.00%)
- top chord-zone usage: 11/168 (safe 93.45%)
- chord pads injected: 11
- style windows: w00-w00:arpeggio, w01-w02:bass_strum, w03-w04:lead_mix, w05-w05:bass_strum, w06-w06:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 3, 'folk_strum': 0, 'lead_mix': 2, 'muted_strum': 0}
