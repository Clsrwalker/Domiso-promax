# Analysis (Guitar Script): 四不可说.mid

## Metrics
- note_count: 287
- duration_s: 88.88828321054527
- tempo0: 62
- tempo_events: 5
- time_sig: 3/4
- max_poly: 7
- bar_density_mean: 9.89655172413793
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 36
- pitch_max: 94

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
- playability: 222/222 (100.00%)
- top chord-zone usage: 8/222 (safe 96.40%)
- chord pads injected: 8
- style windows: w00-w00:bass_strum, w01-w02:lead_mix, w03-w03:arpeggio, w04-w05:bass_strum
- style counts: {'arpeggio': 1, 'bass_strum': 3, 'folk_strum': 0, 'lead_mix': 2, 'muted_strum': 0}
