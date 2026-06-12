# Analysis (Guitar Script): vinland-saga-op-mukanjyo.mid

## Metrics
- note_count: 999
- duration_s: 90.81315789473683
- tempo0: 95
- tempo_events: 1
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 28.542857142857144
- bar_density_p90: 33.4
- tracks: 2
- pitch_min: 24
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
- playability: 330/330 (100.00%)
- top chord-zone usage: 5/330 (safe 98.48%)
- chord pads injected: 5
- style windows: w00-w02:folk_strum, w03-w04:muted_strum, w05-w08:bass_strum
- style counts: {'arpeggio': 0, 'bass_strum': 4, 'folk_strum': 3, 'lead_mix': 0, 'muted_strum': 2}
