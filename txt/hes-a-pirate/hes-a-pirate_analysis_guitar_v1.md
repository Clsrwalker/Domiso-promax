# Analysis (Guitar Script): hes-a-pirate.mid

## Metrics
- note_count: 1285
- duration_s: 78.52857504814025
- tempo0: 207
- tempo_events: 7
- time_sig: 6/8
- max_poly: 6
- bar_density_mean: 14.94186046511628
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 26
- pitch_max: 84

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
- playability: 512/512 (100.00%)
- top chord-zone usage: 0/512 (safe 100.00%)
- chord pads injected: 0
- style windows: w00-w00:arpeggio, w01-w05:lead_mix, w06-w06:folk_strum, w07-w11:bass_strum, w12-w12:folk_strum, w13-w13:arpeggio, w14-w14:lead_mix, w15-w15:folk_strum, w16-w16:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 5, 'folk_strum': 3, 'lead_mix': 6, 'muted_strum': 0}
