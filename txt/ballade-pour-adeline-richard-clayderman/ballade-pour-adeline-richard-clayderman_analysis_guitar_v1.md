# Analysis (Guitar Script): ballade-pour-adeline-richard-clayderman.mid

## Metrics
- note_count: 912
- duration_s: 174.7543530772633
- tempo0: 60
- tempo_events: 11
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 21.209302325581394
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
- pitch_max: 93

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
- playability: 442/442 (100.00%)
- top chord-zone usage: 6/442 (safe 98.64%)
- chord pads injected: 6
- style windows: w00-w01:arpeggio, w02-w04:bass_strum, w05-w05:folk_strum, w06-w08:lead_mix, w09-w10:bass_strum
- style counts: {'arpeggio': 2, 'bass_strum': 5, 'folk_strum': 1, 'lead_mix': 3, 'muted_strum': 0}
