# Analysis (Guitar Script): handclap-fitz-and-the-tantrums.mid

## Metrics
- note_count: 2586
- duration_s: 183.42857142857142
- tempo0: 140
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 24.16822429906542
- bar_density_p90: 34.0
- tracks: 2
- pitch_min: 31
- pitch_max: 96

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
- playability: 1200/1200 (100.00%)
- top chord-zone usage: 18/1200 (safe 98.50%)
- chord pads injected: 18
- style windows: w00-w03:arpeggio, w04-w04:bass_strum, w05-w07:lead_mix, w08-w08:arpeggio, w09-w10:folk_strum, w11-w11:arpeggio, w12-w12:muted_strum, w13-w15:lead_mix, w16-w21:bass_strum, w22-w24:lead_mix, w25-w25:folk_strum, w26-w26:bass_strum
- style counts: {'arpeggio': 6, 'bass_strum': 8, 'folk_strum': 3, 'lead_mix': 9, 'muted_strum': 1}
