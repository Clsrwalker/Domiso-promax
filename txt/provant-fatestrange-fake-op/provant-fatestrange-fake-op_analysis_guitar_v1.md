# Analysis (Guitar Script): provant-fatestrange-fake-op.mid

## Metrics
- note_count: 1329
- duration_s: 87.32038834951456
- tempo0: 206
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.72
- bar_density_p90: 28.0
- tracks: 2
- pitch_min: 22
- pitch_max: 81

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
- playability: 775/775 (100.00%)
- top chord-zone usage: 12/775 (safe 98.45%)
- chord pads injected: 12
- style windows: w00-w08:bass_strum, w09-w17:lead_mix, w18-w18:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 9, 'folk_strum': 0, 'lead_mix': 9, 'muted_strum': 0}
