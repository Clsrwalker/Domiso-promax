# Analysis (Guitar Script): titanium.mid

## Metrics
- note_count: 1664
- duration_s: 202.48888888888888
- tempo0: 135
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 14.725663716814159
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 32
- pitch_max: 87

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
- playability: 1089/1089 (100.00%)
- top chord-zone usage: 62/1089 (safe 94.31%)
- chord pads injected: 62
- style windows: w00-w01:bass_strum, w02-w05:arpeggio, w06-w07:bass_strum, w08-w08:folk_strum, w09-w09:lead_mix, w10-w11:bass_strum, w12-w15:arpeggio, w16-w17:bass_strum, w18-w18:folk_strum, w19-w21:lead_mix, w22-w23:folk_strum, w24-w24:bass_strum, w25-w26:lead_mix, w27-w27:bass_strum, w28-w28:arpeggio
- style counts: {'arpeggio': 9, 'bass_strum': 10, 'folk_strum': 4, 'lead_mix': 6, 'muted_strum': 0}
