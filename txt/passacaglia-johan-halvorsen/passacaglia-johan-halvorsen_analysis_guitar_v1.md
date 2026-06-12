# Analysis (Guitar Script): passacaglia-johan-halvorsen.mid

## Metrics
- note_count: 1030
- duration_s: 136.52307692307693
- tempo0: 130
- tempo_events: 1
- time_sig: 4/4
- max_poly: 3
- bar_density_mean: 13.91891891891892
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 36
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
- playability: 847/847 (100.00%)
- top chord-zone usage: 20/847 (safe 97.64%)
- chord pads injected: 20
- style windows: w00-w08:arpeggio, w09-w15:lead_mix, w16-w18:bass_strum
- style counts: {'arpeggio': 9, 'bass_strum': 3, 'folk_strum': 0, 'lead_mix': 7, 'muted_strum': 0}
