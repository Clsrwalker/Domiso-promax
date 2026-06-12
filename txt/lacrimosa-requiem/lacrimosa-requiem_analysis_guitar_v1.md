# Analysis (Guitar Script): lacrimosa-requiem.mid

## Metrics
- note_count: 698
- duration_s: 168.75
- tempo0: 64
- tempo_events: 1
- time_sig: 12/8
- max_poly: 6
- bar_density_mean: 23.266666666666666
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 33
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
- playability: 513/513 (100.00%)
- top chord-zone usage: 5/513 (safe 99.03%)
- chord pads injected: 5
- style windows: w00-w00:arpeggio, w01-w01:bass_strum, w02-w05:folk_strum, w06-w06:lead_mix, w07-w07:arpeggio, w08-w08:folk_strum, w09-w10:bass_strum, w11-w11:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 3, 'folk_strum': 5, 'lead_mix': 1, 'muted_strum': 0}
