# Analysis (Guitar Script): lu-xiao-yu.mid

## Metrics
- note_count: 545
- duration_s: 78.95454545454545
- tempo0: 88
- tempo_events: 1
- time_sig: 4/4
- max_poly: 3
- bar_density_mean: 18.79310344827586
- bar_density_p90: 24.0
- tracks: 2
- pitch_min: 36
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
- playability: 200/200 (100.00%)
- top chord-zone usage: 22/200 (safe 89.00%)
- chord pads injected: 22
- style windows: w00-w00:arpeggio, w01-w03:folk_strum, w04-w05:lead_mix, w06-w07:bass_strum
- style counts: {'arpeggio': 1, 'bass_strum': 2, 'folk_strum': 3, 'lead_mix': 2, 'muted_strum': 0}
