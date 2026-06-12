# Analysis (Guitar Script): cancan-offenbach.mid

## Metrics
- note_count: 2094
- duration_s: 131.08928571428572
- tempo0: 160
- tempo_events: 5
- time_sig: 1/2
- max_poly: 7
- bar_density_mean: 12.104046242774567
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 33
- pitch_max: 98

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
- playability: 876/876 (100.00%)
- top chord-zone usage: 7/876 (safe 99.20%)
- chord pads injected: 7
- style windows: w00-w01:arpeggio, w02-w02:folk_strum, w03-w03:lead_mix, w04-w10:bass_strum, w11-w11:lead_mix, w12-w16:muted_strum, w17-w17:bass_strum, w18-w18:arpeggio, w19-w20:folk_strum, w21-w21:muted_strum
- style counts: {'arpeggio': 3, 'bass_strum': 8, 'folk_strum': 3, 'lead_mix': 2, 'muted_strum': 6}
