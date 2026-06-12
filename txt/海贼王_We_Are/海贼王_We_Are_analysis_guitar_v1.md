# Analysis (Guitar Script): 海贼王_We_Are.mid

## Metrics
- note_count: 1155
- duration_s: 144.5
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.821917808219178
- bar_density_p90: 22.6
- tracks: 2
- pitch_min: 31
- pitch_max: 87

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
- playability: 799/799 (100.00%)
- top chord-zone usage: 28/799 (safe 96.50%)
- chord pads injected: 28
- style windows: w00-w01:bass_strum, w02-w02:arpeggio, w03-w03:muted_strum, w04-w04:lead_mix, w05-w07:bass_strum, w08-w08:arpeggio, w09-w11:folk_strum, w12-w12:arpeggio, w13-w15:bass_strum, w16-w18:arpeggio
- style counts: {'arpeggio': 6, 'bass_strum': 8, 'folk_strum': 3, 'lead_mix': 1, 'muted_strum': 1}
