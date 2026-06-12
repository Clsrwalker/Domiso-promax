# Analysis (Guitar Script): fan-fang-xiang-de-zhong-zhou-jie-lun.mid

## Metrics
- note_count: 1770
- duration_s: 259.258064516129
- tempo0: 80
- tempo_events: 2
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 17.87878787878788
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 31
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
- playability: 1291/1291 (100.00%)
- top chord-zone usage: 32/1291 (safe 97.52%)
- chord pads injected: 32
- style windows: w00-w01:bass_strum, w02-w02:folk_strum, w03-w03:muted_strum, w04-w07:arpeggio, w08-w11:muted_strum, w12-w12:bass_strum, w13-w13:folk_strum, w14-w15:lead_mix, w16-w16:folk_strum, w17-w17:arpeggio, w18-w21:muted_strum, w22-w24:bass_strum
- style counts: {'arpeggio': 5, 'bass_strum': 6, 'folk_strum': 3, 'lead_mix': 2, 'muted_strum': 9}
