# Analysis (Guitar Script): 王国城堡1.mid

## Metrics
- note_count: 155
- duration_s: 41.620535714285715
- tempo0: 105
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 8.61111111111111
- bar_density_p90: 11.3
- tracks: 2
- pitch_min: 41
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
- playability: 104/104 (100.00%)
- top chord-zone usage: 17/104 (safe 83.65%)
- chord pads injected: 17
- style windows: w00-w01:lead_mix, w02-w02:bass_strum, w03-w04:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 1, 'folk_strum': 0, 'lead_mix': 2, 'muted_strum': 0}
