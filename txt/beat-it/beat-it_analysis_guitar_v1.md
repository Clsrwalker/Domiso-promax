# Analysis (Guitar Script): beat-it.mid

## Metrics
- note_count: 1282
- duration_s: 116.0
- tempo0: 135
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 19.424242424242426
- bar_density_p90: 22.0
- tracks: 4
- pitch_min: 36
- pitch_max: 84

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
- playability: 953/953 (100.00%)
- top chord-zone usage: 22/953 (safe 97.69%)
- chord pads injected: 22
- style windows: w00-w01:bass_strum, w02-w05:lead_mix, w06-w07:bass_strum, w08-w09:folk_strum, w10-w10:arpeggio, w11-w12:lead_mix, w13-w14:bass_strum, w15-w15:folk_strum, w16-w16:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 6, 'folk_strum': 3, 'lead_mix': 6, 'muted_strum': 0}
