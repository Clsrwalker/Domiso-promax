# Analysis (Guitar Script): ennio-morricone-enduring-movement.mid

## Metrics
- note_count: 1681
- duration_s: 80.32575334821429
- tempo0: 168
- tempo_events: 3
- time_sig: 2/4
- max_poly: 7
- bar_density_mean: 15.144144144144144
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 21
- pitch_max: 99

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
- playability: 762/762 (100.00%)
- top chord-zone usage: 0/762 (safe 100.00%)
- chord pads injected: 0
- style windows: w00-w06:bass_strum, w07-w07:folk_strum, w08-w12:muted_strum, w13-w13:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 7, 'folk_strum': 1, 'lead_mix': 0, 'muted_strum': 5}
