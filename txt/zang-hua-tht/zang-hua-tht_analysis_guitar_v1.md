# Analysis (Guitar Script): zang-hua-tht.mid

## Metrics
- note_count: 1606
- duration_s: 235.46341463414635
- tempo0: 164
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 10.0375
- bar_density_p90: 14.9
- tracks: 2
- pitch_min: 46
- pitch_max: 89

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
- playability: 1330/1330 (100.00%)
- top chord-zone usage: 74/1330 (safe 94.44%)
- chord pads injected: 74
- style windows: w00-w07:bass_strum, w08-w09:lead_mix, w10-w11:muted_strum, w12-w16:lead_mix, w17-w35:bass_strum, w36-w36:lead_mix, w37-w37:muted_strum, w38-w38:bass_strum, w39-w40:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 28, 'folk_strum': 0, 'lead_mix': 8, 'muted_strum': 3}
