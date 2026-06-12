# Analysis (Guitar Script): 那天下雨了_zhoujielun.mid

## Metrics
- note_count: 999
- duration_s: 214.05405405405406
- tempo0: 74
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 15.136363636363637
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 33
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
- playability: 731/731 (100.00%)
- top chord-zone usage: 29/731 (safe 96.03%)
- chord pads injected: 29
- style windows: w00-w01:bass_strum, w02-w02:folk_strum, w03-w05:lead_mix, w06-w06:arpeggio, w07-w07:bass_strum, w08-w09:lead_mix, w10-w11:arpeggio, w12-w13:folk_strum, w14-w15:lead_mix, w16-w16:arpeggio
- style counts: {'arpeggio': 4, 'bass_strum': 3, 'folk_strum': 3, 'lead_mix': 7, 'muted_strum': 0}
