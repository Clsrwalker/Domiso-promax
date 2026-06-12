# Analysis (Guitar Script): 时间煮雨.mid

## Metrics
- note_count: 1000
- duration_s: 250.5375512995896
- tempo0: 85
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 11.363636363636363
- bar_density_p90: 15.2
- tracks: 2
- pitch_min: 38
- pitch_max: 91

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
- playability: 963/963 (100.00%)
- top chord-zone usage: 63/963 (safe 93.46%)
- chord pads injected: 63
- style windows: w00-w00:lead_mix, w01-w06:bass_strum, w07-w07:muted_strum, w08-w08:lead_mix, w09-w14:bass_strum, w15-w18:lead_mix, w19-w19:folk_strum, w20-w20:bass_strum, w21-w22:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 13, 'folk_strum': 1, 'lead_mix': 6, 'muted_strum': 1}
