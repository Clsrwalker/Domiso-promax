# Analysis (Guitar Script): avid-sawanohiroyukinzkmizuki.mid

## Metrics
- note_count: 2468
- duration_s: 185.57115384615386
- tempo0: 120
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 26.82608695652174
- bar_density_p90: 40.0
- tracks: 2
- pitch_min: 33
- pitch_max: 103

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
- playability: 1084/1084 (100.00%)
- top chord-zone usage: 64/1084 (safe 94.10%)
- chord pads injected: 64
- style windows: w00-w03:arpeggio, w04-w08:bass_strum, w09-w09:arpeggio, w10-w10:lead_mix, w11-w13:bass_strum, w14-w14:folk_strum, w15-w15:lead_mix, w16-w16:muted_strum, w17-w17:bass_strum, w18-w18:folk_strum, w19-w21:lead_mix, w22-w23:arpeggio
- style counts: {'arpeggio': 7, 'bass_strum': 9, 'folk_strum': 2, 'lead_mix': 5, 'muted_strum': 1}
