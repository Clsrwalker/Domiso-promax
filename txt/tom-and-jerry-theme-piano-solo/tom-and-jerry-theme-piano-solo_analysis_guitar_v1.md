# Analysis (Guitar Script): tom-and-jerry-theme-piano-solo.mid

## Metrics
- note_count: 243
- duration_s: 25.92650002327421
- tempo0: 165
- tempo_events: 5
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 12.15
- bar_density_p90: 19.6
- tracks: 2
- pitch_min: 33
- pitch_max: 79

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
- playability: 170/170 (100.00%)
- top chord-zone usage: 1/170 (safe 99.41%)
- chord pads injected: 1
- style windows: w00-w01:muted_strum, w02-w03:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 0, 'folk_strum': 0, 'lead_mix': 0, 'muted_strum': 2}
