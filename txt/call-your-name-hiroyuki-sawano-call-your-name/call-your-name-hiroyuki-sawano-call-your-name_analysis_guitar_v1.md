# Analysis (Guitar Script): call-your-name-hiroyuki-sawano-call-your-name.mid

## Metrics
- note_count: 1556
- duration_s: 261.4931972789115
- tempo0: 70
- tempo_events: 4
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 20.473684210526315
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 23
- pitch_max: 85

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
- playability: 711/711 (100.00%)
- top chord-zone usage: 17/711 (safe 97.61%)
- chord pads injected: 17
- style windows: w00-w04:bass_strum, w05-w06:muted_strum, w07-w07:lead_mix, w08-w08:bass_strum, w09-w09:folk_strum, w10-w12:muted_strum, w13-w13:folk_strum, w14-w14:bass_strum, w15-w15:muted_strum, w16-w16:folk_strum, w17-w18:bass_strum, w19-w19:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 9, 'folk_strum': 3, 'lead_mix': 1, 'muted_strum': 6}
