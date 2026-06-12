# Analysis (Guitar Script): plants-vs-zombies-grasswalk.mid

## Metrics
- note_count: 808
- duration_s: 151.475
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 10.631578947368421
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 29
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
- playability: 731/731 (100.00%)
- top chord-zone usage: 55/731 (safe 92.48%)
- chord pads injected: 55
- style windows: w00-w01:arpeggio, w02-w03:folk_strum, w04-w05:lead_mix, w06-w06:arpeggio, w07-w13:muted_strum, w14-w14:bass_strum, w15-w17:lead_mix, w18-w18:bass_strum
- style counts: {'arpeggio': 3, 'bass_strum': 2, 'folk_strum': 2, 'lead_mix': 5, 'muted_strum': 7}
