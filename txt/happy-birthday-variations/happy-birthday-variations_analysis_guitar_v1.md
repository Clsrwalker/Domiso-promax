# Analysis (Guitar Script): happy-birthday-variations.mid

## Metrics
- note_count: 2588
- duration_s: 320.7031096354626
- tempo0: 65
- tempo_events: 21
- time_sig: 1/4
- max_poly: 9
- bar_density_mean: 4.1877022653721685
- bar_density_p90: 7.0
- tracks: 2
- pitch_min: 25
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
- playability: 1588/1588 (100.00%)
- top chord-zone usage: 29/1588 (safe 98.17%)
- chord pads injected: 29
- style windows: w00-w00:muted_strum, w01-w01:lead_mix, w02-w04:folk_strum, w05-w06:arpeggio, w07-w07:folk_strum, w08-w09:lead_mix, w10-w11:folk_strum, w12-w12:muted_strum, w13-w15:arpeggio, w16-w22:lead_mix, w23-w32:bass_strum, w33-w35:arpeggio, w36-w37:folk_strum, w38-w38:bass_strum
- style counts: {'arpeggio': 8, 'bass_strum': 11, 'folk_strum': 8, 'lead_mix': 10, 'muted_strum': 2}
