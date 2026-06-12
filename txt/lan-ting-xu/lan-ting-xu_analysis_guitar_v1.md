# Analysis (Guitar Script): lan-ting-xu.mid

## Metrics
- note_count: 743
- duration_s: 186.1578947368421
- tempo0: 76
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 12.59322033898305
- bar_density_p90: 16.0
- tracks: 2
- pitch_min: 33
- pitch_max: 83

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
- playability: 729/729 (100.00%)
- top chord-zone usage: 37/729 (safe 94.92%)
- chord pads injected: 36
- style windows: w00-w01:arpeggio, w02-w04:bass_strum, w05-w06:lead_mix, w07-w10:arpeggio, w11-w13:muted_strum, w14-w14:arpeggio
- style counts: {'arpeggio': 7, 'bass_strum': 3, 'folk_strum': 0, 'lead_mix': 2, 'muted_strum': 3}
