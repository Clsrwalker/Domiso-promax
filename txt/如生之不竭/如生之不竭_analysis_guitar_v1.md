# Analysis (Guitar Script): 如生之不竭.mid

## Metrics
- note_count: 1562
- duration_s: 151.69811320754715
- tempo0: 106
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 23.313432835820894
- bar_density_p90: 33.4
- tracks: 2
- pitch_min: 38
- pitch_max: 95

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
- playability: 562/562 (100.00%)
- top chord-zone usage: 7/562 (safe 98.75%)
- chord pads injected: 7
- style windows: w00-w03:arpeggio, w04-w04:lead_mix, w05-w07:bass_strum, w08-w08:arpeggio, w09-w09:lead_mix, w10-w11:folk_strum, w12-w12:lead_mix, w13-w15:muted_strum, w16-w16:bass_strum
- style counts: {'arpeggio': 5, 'bass_strum': 4, 'folk_strum': 2, 'lead_mix': 3, 'muted_strum': 3}
