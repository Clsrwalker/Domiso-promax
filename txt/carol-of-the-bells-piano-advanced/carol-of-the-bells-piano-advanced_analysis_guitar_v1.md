# Analysis (Guitar Script): carol-of-the-bells-piano-advanced.mid

## Metrics
- note_count: 1817
- duration_s: 156.69772727272726
- tempo0: 150
- tempo_events: 5
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.813725490196077
- bar_density_p90: 30.0
- tracks: 2
- pitch_min: 24
- pitch_max: 105

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
- playability: 839/839 (100.00%)
- top chord-zone usage: 21/839 (safe 97.50%)
- chord pads injected: 21
- style windows: w00-w04:bass_strum, w05-w05:folk_strum, w06-w09:lead_mix, w10-w11:folk_strum, w12-w12:muted_strum, w13-w15:lead_mix, w16-w16:muted_strum, w17-w18:bass_strum, w19-w21:arpeggio, w22-w23:folk_strum, w24-w24:bass_strum, w25-w25:arpeggio
- style counts: {'arpeggio': 4, 'bass_strum': 8, 'folk_strum': 5, 'lead_mix': 7, 'muted_strum': 2}
