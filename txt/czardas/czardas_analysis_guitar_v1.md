# Analysis (Guitar Script): czardas.mid

## Metrics
- note_count: 2403
- duration_s: 268.61831376129766
- tempo0: 55
- tempo_events: 15
- time_sig: 2/4
- max_poly: 8
- bar_density_mean: 12.075376884422111
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 31
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
- playability: 1351/1351 (100.00%)
- top chord-zone usage: 33/1351 (safe 97.56%)
- chord pads injected: 33
- style windows: w00-w06:bass_strum, w07-w09:folk_strum, w10-w14:lead_mix, w15-w18:bass_strum, w19-w19:lead_mix, w20-w21:folk_strum, w22-w23:lead_mix, w24-w24:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 11, 'folk_strum': 5, 'lead_mix': 8, 'muted_strum': 0}
