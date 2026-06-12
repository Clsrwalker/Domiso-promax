# Analysis (Guitar Script): closer-the-chainsmokers.mid

## Metrics
- note_count: 482
- duration_s: 106.66805555555555
- tempo0: 90
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 12.05
- bar_density_p90: 17.9
- tracks: 2
- pitch_min: 36
- pitch_max: 86

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
- playability: 338/338 (100.00%)
- top chord-zone usage: 7/338 (safe 97.93%)
- chord pads injected: 7
- style windows: w00-w02:bass_strum, w03-w03:lead_mix, w04-w04:muted_strum, w05-w06:arpeggio, w07-w08:lead_mix, w09-w09:bass_strum
- style counts: {'arpeggio': 2, 'bass_strum': 4, 'folk_strum': 0, 'lead_mix': 3, 'muted_strum': 1}
