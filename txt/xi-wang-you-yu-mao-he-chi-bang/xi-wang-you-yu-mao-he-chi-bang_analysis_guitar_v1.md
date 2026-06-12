# Analysis (Guitar Script): xi-wang-you-yu-mao-he-chi-bang.mid

## Metrics
- note_count: 2284
- duration_s: 240.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.033333333333335
- bar_density_p90: 26.0
- tracks: 2
- pitch_min: 37
- pitch_max: 100

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
- playability: 1350/1350 (100.00%)
- top chord-zone usage: 43/1350 (safe 96.81%)
- chord pads injected: 43
- style windows: w00-w04:bass_strum, w05-w05:lead_mix, w06-w07:arpeggio, w08-w09:lead_mix, w10-w10:muted_strum, w11-w15:folk_strum, w16-w16:muted_strum, w17-w19:lead_mix, w20-w23:bass_strum, w24-w25:lead_mix, w26-w27:folk_strum, w28-w29:bass_strum, w30-w30:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 11, 'folk_strum': 7, 'lead_mix': 8, 'muted_strum': 2}
