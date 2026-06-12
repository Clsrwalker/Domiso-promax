# Analysis (Guitar Script): g-minor-bach.mid

## Metrics
- note_count: 1810
- duration_s: 158.28
- tempo0: 100
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 27.424242424242426
- bar_density_p90: 34.0
- tracks: 3
- pitch_min: 34
- pitch_max: 80

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
- playability: 817/817 (100.00%)
- top chord-zone usage: 3/817 (safe 99.63%)
- chord pads injected: 3
- style windows: w00-w06:arpeggio, w07-w14:folk_strum, w15-w16:bass_strum
- style counts: {'arpeggio': 7, 'bass_strum': 2, 'folk_strum': 8, 'lead_mix': 0, 'muted_strum': 0}
