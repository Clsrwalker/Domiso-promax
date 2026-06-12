# Analysis (Guitar Script): rush_e_real.mid

## Metrics
- note_count: 46291
- duration_s: 141.2309105390356
- tempo0: 120
- tempo_events: 103
- time_sig: 4/4
- max_poly: 164
- bar_density_mean: 585.9620253164557
- bar_density_p90: 1096.0
- tracks: 12
- pitch_min: 0
- pitch_max: 127

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
- playability: 828/828 (100.00%)
- top chord-zone usage: 12/828 (safe 98.55%)
- chord pads injected: 10
- style windows: w00-w07:arpeggio, w08-w12:folk_strum, w13-w13:bass_strum, w14-w19:lead_mix, w20-w20:arpeggio
- style counts: {'arpeggio': 9, 'bass_strum': 1, 'folk_strum': 5, 'lead_mix': 6, 'muted_strum': 0}
