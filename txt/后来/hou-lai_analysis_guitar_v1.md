# Analysis (Guitar Script): hou-lai.mid

## Metrics
- note_count: 1465
- duration_s: 316.8
- tempo0: 75
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 14.797979797979798
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 24
- pitch_max: 98

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
- playability: 1216/1216 (100.00%)
- top chord-zone usage: 59/1216 (safe 95.15%)
- chord pads injected: 58
- style windows: w00-w09:arpeggio, w10-w11:lead_mix, w12-w13:folk_strum, w14-w14:bass_strum, w15-w19:lead_mix, w20-w20:muted_strum, w21-w24:bass_strum
- style counts: {'arpeggio': 10, 'bass_strum': 5, 'folk_strum': 2, 'lead_mix': 7, 'muted_strum': 1}
