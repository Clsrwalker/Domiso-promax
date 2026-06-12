# Analysis (Guitar Script): man-leng.mid

## Metrics
- note_count: 1007
- duration_s: 195.9183673469388
- tempo0: 98
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 12.5875
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 40
- pitch_max: 83

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
- playability: 866/866 (100.00%)
- top chord-zone usage: 66/866 (safe 92.38%)
- chord pads injected: 66
- style windows: w00-w01:bass_strum, w02-w05:arpeggio, w06-w06:bass_strum, w07-w09:lead_mix, w10-w11:arpeggio, w12-w12:bass_strum, w13-w18:lead_mix, w19-w19:bass_strum, w20-w20:arpeggio
- style counts: {'arpeggio': 7, 'bass_strum': 5, 'folk_strum': 0, 'lead_mix': 9, 'muted_strum': 0}
