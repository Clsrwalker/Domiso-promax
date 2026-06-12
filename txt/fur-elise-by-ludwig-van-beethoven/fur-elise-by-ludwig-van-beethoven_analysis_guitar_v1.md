# Analysis (Guitar Script): fur-elise-by-ludwig-van-beethoven.mid

## Metrics
- note_count: 1041
- duration_s: 94.0
- tempo0: 120
- tempo_events: 1
- time_sig: 1/8
- max_poly: 6
- bar_density_mean: 2.783422459893048
- bar_density_p90: 5.0
- tracks: 2
- pitch_min: 33
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
- playability: 566/566 (100.00%)
- top chord-zone usage: 5/566 (safe 99.12%)
- chord pads injected: 5
- style windows: w00-w00:arpeggio, w01-w02:folk_strum, w03-w03:arpeggio, w04-w04:muted_strum, w05-w05:lead_mix, w06-w07:folk_strum, w08-w08:muted_strum, w09-w09:lead_mix, w10-w10:arpeggio, w11-w11:bass_strum
- style counts: {'arpeggio': 3, 'bass_strum': 1, 'folk_strum': 4, 'lead_mix': 2, 'muted_strum': 2}
