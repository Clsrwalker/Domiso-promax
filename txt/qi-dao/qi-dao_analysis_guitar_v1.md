# Analysis (Guitar Script): qi-dao.mid

## Metrics
- note_count: 1028
- duration_s: 187.78509054478917
- tempo0: 76
- tempo_events: 4
- time_sig: 1/4
- max_poly: 6
- bar_density_mean: 4.3559322033898304
- bar_density_p90: 6.0
- tracks: 2
- pitch_min: 33
- pitch_max: 95

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
- playability: 822/822 (100.00%)
- top chord-zone usage: 29/822 (safe 96.47%)
- chord pads injected: 29
- style windows: w00-w05:bass_strum, w06-w06:folk_strum, w07-w07:arpeggio, w08-w11:bass_strum, w12-w12:lead_mix, w13-w13:muted_strum, w14-w14:bass_strum
- style counts: {'arpeggio': 1, 'bass_strum': 11, 'folk_strum': 1, 'lead_mix': 1, 'muted_strum': 1}
