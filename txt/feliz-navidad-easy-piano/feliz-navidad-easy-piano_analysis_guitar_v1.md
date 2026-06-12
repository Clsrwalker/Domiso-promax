# Analysis (Guitar Script): feliz-navidad-easy-piano.mid

## Metrics
- note_count: 320
- duration_s: 63.916666666666664
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 10.0
- bar_density_p90: 16.7
- tracks: 2
- pitch_min: 48
- pitch_max: 76

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
- playability: 216/216 (100.00%)
- top chord-zone usage: 3/216 (safe 98.61%)
- chord pads injected: 3
- style windows: w00-w02:bass_strum, w03-w03:muted_strum, w04-w04:folk_strum, w05-w05:bass_strum, w06-w07:lead_mix
- style counts: {'arpeggio': 0, 'bass_strum': 4, 'folk_strum': 1, 'lead_mix': 2, 'muted_strum': 1}
