# Analysis (Guitar Script): auroras-theme-child-of-light.mid

## Metrics
- note_count: 933
- duration_s: 162.78846153846155
- tempo0: 65
- tempo_events: 2
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.4375
- bar_density_p90: 29.1
- tracks: 2
- pitch_min: 36
- pitch_max: 103

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
- playability: 446/446 (100.00%)
- top chord-zone usage: 24/446 (safe 94.62%)
- chord pads injected: 24
- style windows: w00-w01:arpeggio, w02-w08:folk_strum, w09-w09:muted_strum, w10-w11:bass_strum, w12-w12:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 2, 'folk_strum': 7, 'lead_mix': 0, 'muted_strum': 1}
