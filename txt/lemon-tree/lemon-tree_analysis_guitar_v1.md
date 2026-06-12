# Analysis (Guitar Script): lemon-tree.mid

## Metrics
- note_count: 1471
- duration_s: 193.62857142857143
- tempo0: 140
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 13.017699115044248
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 43
- pitch_max: 77

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
- playability: 895/895 (100.00%)
- top chord-zone usage: 58/895 (safe 93.52%)
- chord pads injected: 58
- style windows: w00-w01:arpeggio, w02-w07:folk_strum, w08-w10:lead_mix, w11-w11:muted_strum, w12-w16:folk_strum, w17-w17:bass_strum, w18-w18:arpeggio, w19-w23:lead_mix, w24-w24:folk_strum, w25-w25:arpeggio, w26-w27:bass_strum, w28-w28:arpeggio
- style counts: {'arpeggio': 5, 'bass_strum': 3, 'folk_strum': 12, 'lead_mix': 8, 'muted_strum': 1}
