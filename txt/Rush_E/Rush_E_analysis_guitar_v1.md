# Analysis (Guitar Script): Rush_E.mid

## Metrics
- note_count: 1842
- duration_s: 179.43580538189738
- tempo0: 70
- tempo_events: 186
- time_sig: 4/4
- max_poly: 57
- bar_density_mean: 11.883870967741936
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 25
- pitch_max: 108

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
- playability: 1391/1391 (100.00%)
- top chord-zone usage: 50/1391 (safe 96.41%)
- chord pads injected: 50
- style windows: w00-w01:arpeggio, w02-w38:bass_strum
- style counts: {'arpeggio': 2, 'bass_strum': 37, 'folk_strum': 0, 'lead_mix': 0, 'muted_strum': 0}
