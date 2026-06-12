# Analysis (Guitar Script): windy-hill.mid

## Metrics
- note_count: 1515
- duration_s: 283.1666516635386
- tempo0: 74
- tempo_events: 8
- time_sig: 1/4
- max_poly: 6
- bar_density_mean: 4.40406976744186
- bar_density_p90: 7.0
- tracks: 2
- pitch_min: 35
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
- playability: 1059/1059 (100.00%)
- top chord-zone usage: 46/1059 (safe 95.66%)
- chord pads injected: 46
- style windows: w00-w03:folk_strum, w04-w07:bass_strum, w08-w10:lead_mix, w11-w11:folk_strum, w12-w15:bass_strum, w16-w16:folk_strum, w17-w19:lead_mix, w20-w21:bass_strum
- style counts: {'arpeggio': 0, 'bass_strum': 10, 'folk_strum': 6, 'lead_mix': 6, 'muted_strum': 0}
