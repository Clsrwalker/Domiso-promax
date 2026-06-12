# Analysis (Guitar Script): fan-wu-tuo-bang.mid

## Metrics
- note_count: 1140
- duration_s: 148.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.405405405405405
- bar_density_p90: 21.0
- tracks: 2
- pitch_min: 43
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
- playability: 789/789 (100.00%)
- top chord-zone usage: 11/789 (safe 98.61%)
- chord pads injected: 11
- style windows: w00-w00:folk_strum, w01-w04:bass_strum, w05-w08:lead_mix, w09-w11:bass_strum, w12-w13:lead_mix, w14-w18:arpeggio
- style counts: {'arpeggio': 5, 'bass_strum': 7, 'folk_strum': 1, 'lead_mix': 6, 'muted_strum': 0}
