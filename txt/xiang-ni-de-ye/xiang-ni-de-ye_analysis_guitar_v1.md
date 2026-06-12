# Analysis (Guitar Script): xiang-ni-de-ye.mid

## Metrics
- note_count: 476
- duration_s: 127.17857142857142
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 12.864864864864865
- bar_density_p90: 16.2
- tracks: 2
- pitch_min: 41
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
- playability: 415/415 (100.00%)
- top chord-zone usage: 21/415 (safe 94.94%)
- chord pads injected: 21
- style windows: w00-w03:bass_strum, w04-w07:folk_strum, w08-w08:lead_mix, w09-w09:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 4, 'folk_strum': 4, 'lead_mix': 1, 'muted_strum': 0}
