# Analysis (Guitar Script): shape-of-my-heart.mid

## Metrics
- note_count: 991
- duration_s: 168.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 11.797619047619047
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 28
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
- playability: 856/856 (100.00%)
- top chord-zone usage: 50/856 (safe 94.16%)
- chord pads injected: 49
- style windows: w00-w10:lead_mix, w11-w14:muted_strum, w15-w17:folk_strum, w18-w19:muted_strum, w20-w20:bass_strum, w21-w21:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 1, 'folk_strum': 3, 'lead_mix': 11, 'muted_strum': 6}
