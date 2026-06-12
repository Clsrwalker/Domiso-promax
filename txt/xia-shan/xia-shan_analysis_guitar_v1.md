# Analysis (Guitar Script): xia-shan.mid

## Metrics
- note_count: 1411
- duration_s: 169.609756097561
- tempo0: 82
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 24.32758620689655
- bar_density_p90: 31.0
- tracks: 2
- pitch_min: 32
- pitch_max: 90

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
- playability: 916/916 (100.00%)
- top chord-zone usage: 4/916 (safe 99.56%)
- chord pads injected: 4
- style windows: w00-w01:bass_strum, w02-w02:arpeggio, w03-w03:lead_mix, w04-w04:muted_strum, w05-w05:bass_strum, w06-w07:folk_strum, w08-w08:lead_mix, w09-w13:bass_strum, w14-w14:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 8, 'folk_strum': 2, 'lead_mix': 2, 'muted_strum': 1}
