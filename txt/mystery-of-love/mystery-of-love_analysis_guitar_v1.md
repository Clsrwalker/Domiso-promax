# Analysis (Guitar Script): mystery-of-love.mid

## Metrics
- note_count: 1571
- duration_s: 201.85
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 15.71
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 47
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
- playability: 931/931 (100.00%)
- top chord-zone usage: 30/931 (safe 96.78%)
- chord pads injected: 30
- style windows: w00-w00:arpeggio, w01-w01:lead_mix, w02-w05:bass_strum, w06-w06:muted_strum, w07-w07:lead_mix, w08-w08:folk_strum, w09-w09:arpeggio, w10-w13:muted_strum, w14-w14:lead_mix, w15-w15:folk_strum, w16-w16:arpeggio, w17-w21:bass_strum, w22-w22:arpeggio, w23-w24:folk_strum, w25-w25:arpeggio
- style counts: {'arpeggio': 5, 'bass_strum': 9, 'folk_strum': 4, 'lead_mix': 3, 'muted_strum': 5}
