# Analysis (Guitar Script): ni-de-bei-bao.mid

## Metrics
- note_count: 1325
- duration_s: 205.53214285714284
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 22.45762711864407
- bar_density_p90: 29.0
- tracks: 2
- pitch_min: 25
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
- playability: 810/810 (100.00%)
- top chord-zone usage: 26/810 (safe 96.79%)
- chord pads injected: 26
- style windows: w00-w01:bass_strum, w02-w04:lead_mix, w05-w11:folk_strum, w12-w12:lead_mix, w13-w14:bass_strum
- style counts: {'arpeggio': 0, 'bass_strum': 4, 'folk_strum': 7, 'lead_mix': 4, 'muted_strum': 0}
