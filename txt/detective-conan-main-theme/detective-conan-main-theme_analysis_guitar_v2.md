# Analysis (Guitar Script): detective-conan-main-theme.mid

## Metrics
- note_count: 2224
- duration_s: 184.87263858897362
- tempo0: 145
- tempo_events: 4
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 21.59223300970874
- bar_density_p90: 28.6
- tracks: 2
- pitch_min: 24
- pitch_max: 108

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
- playability: 1285/1285 (100.00%)
- top chord-zone usage: 48/1285 (safe 96.26%)
- chord pads injected: 48
- style windows: w00-w01:folk_strum, w02-w06:bass_strum, w07-w07:arpeggio, w08-w08:lead_mix, w09-w11:muted_strum, w12-w12:lead_mix, w13-w13:folk_strum, w14-w16:bass_strum, w17-w17:folk_strum, w18-w18:arpeggio, w19-w23:lead_mix, w24-w24:folk_strum, w25-w25:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 8, 'folk_strum': 5, 'lead_mix': 7, 'muted_strum': 3}
