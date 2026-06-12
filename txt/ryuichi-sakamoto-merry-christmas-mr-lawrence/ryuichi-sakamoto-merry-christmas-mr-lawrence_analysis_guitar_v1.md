# Analysis (Guitar Script): ryuichi-sakamoto-merry-christmas-mr-lawrence.mid

## Metrics
- note_count: 2195
- duration_s: 335.6031583264971
- tempo0: 53
- tempo_events: 2
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 29.66216216216216
- bar_density_p90: 59.5
- tracks: 2
- pitch_min: 29
- pitch_max: 101

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
- playability: 1035/1035 (100.00%)
- top chord-zone usage: 21/1035 (safe 97.97%)
- chord pads injected: 21
- style windows: w00-w05:arpeggio, w06-w17:bass_strum, w18-w19:lead_mix, w20-w27:muted_strum
- style counts: {'arpeggio': 6, 'bass_strum': 12, 'folk_strum': 0, 'lead_mix': 2, 'muted_strum': 8}
