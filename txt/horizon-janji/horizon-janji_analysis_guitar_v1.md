# Analysis (Guitar Script): horizon-janji.mid

## Metrics
- note_count: 1984
- duration_s: 187.5009765625
- tempo0: 128
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 19.84
- bar_density_p90: 41.0
- tracks: 2
- pitch_min: 42
- pitch_max: 92

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
- playability: 922/922 (100.00%)
- top chord-zone usage: 52/922 (safe 94.36%)
- chord pads injected: 46
- style windows: w00-w03:bass_strum, w04-w05:muted_strum, w06-w07:folk_strum, w08-w09:muted_strum, w10-w11:folk_strum, w12-w17:bass_strum, w18-w22:muted_strum, w23-w24:bass_strum, w25-w25:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 12, 'folk_strum': 4, 'lead_mix': 0, 'muted_strum': 9}
