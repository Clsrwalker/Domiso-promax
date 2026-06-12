# Analysis (Guitar Script): Billie_Jean.mid

## Metrics
- note_count: 5972
- duration_s: 294.91525423728814
- tempo0: 118
- tempo_events: 1
- time_sig: 4/4
- max_poly: 13
- bar_density_mean: 41.186206896551724
- bar_density_p90: 50.0
- tracks: 9
- pitch_min: 30
- pitch_max: 85

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
- playability: 1685/1685 (100.00%)
- top chord-zone usage: 0/1685 (safe 100.00%)
- chord pads injected: 0
- style windows: w00-w08:arpeggio, w09-w10:bass_strum, w11-w14:folk_strum, w15-w18:arpeggio, w19-w20:bass_strum, w21-w21:folk_strum, w22-w23:muted_strum, w24-w25:folk_strum, w26-w27:muted_strum, w28-w30:folk_strum, w31-w34:muted_strum, w35-w35:lead_mix, w36-w36:arpeggio
- style counts: {'arpeggio': 14, 'bass_strum': 4, 'folk_strum': 10, 'lead_mix': 1, 'muted_strum': 8}
