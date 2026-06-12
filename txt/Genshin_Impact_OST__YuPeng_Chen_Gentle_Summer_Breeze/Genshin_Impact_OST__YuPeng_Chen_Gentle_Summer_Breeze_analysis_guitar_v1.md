# Analysis (Guitar Script): Genshin_Impact_OST__YuPeng_Chen_Gentle_Summer_Breeze.mid

## Metrics
- note_count: 208
- duration_s: 54.31825980392156
- tempo0: 85
- tempo_events: 3
- time_sig: 3/4
- max_poly: 7
- bar_density_mean: 8.0
- bar_density_p90: 11.0
- tracks: 2
- pitch_min: 43
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
- playability: 180/180 (100.00%)
- top chord-zone usage: 9/180 (safe 95.00%)
- chord pads injected: 9
- style windows: w00-w01:bass_strum, w02-w02:muted_strum, w03-w03:lead_mix, w04-w04:bass_strum
- style counts: {'arpeggio': 0, 'bass_strum': 3, 'folk_strum': 0, 'lead_mix': 1, 'muted_strum': 1}
