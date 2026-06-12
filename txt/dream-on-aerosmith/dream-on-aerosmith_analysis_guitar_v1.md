# Analysis (Guitar Script): dream-on-aerosmith.mid

## Metrics
- note_count: 2020
- duration_s: 261.53685897435895
- tempo0: 78
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 24.047619047619047
- bar_density_p90: 34.0
- tracks: 2
- pitch_min: 29
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
- playability: 1265/1265 (100.00%)
- top chord-zone usage: 13/1265 (safe 98.97%)
- chord pads injected: 13
- style windows: w00-w04:bass_strum, w05-w05:folk_strum, w06-w06:muted_strum, w07-w09:bass_strum, w10-w10:lead_mix, w11-w11:folk_strum, w12-w12:arpeggio, w13-w19:lead_mix, w20-w20:folk_strum
- style counts: {'arpeggio': 1, 'bass_strum': 8, 'folk_strum': 3, 'lead_mix': 8, 'muted_strum': 1}
