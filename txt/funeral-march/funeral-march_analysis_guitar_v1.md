# Analysis (Guitar Script): funeral-march.mid

## Metrics
- note_count: 2106
- duration_s: 539.875
- tempo0: 48
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 19.5
- bar_density_p90: 31.0
- tracks: 2
- pitch_min: 25
- pitch_max: 89

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
- playability: 1157/1157 (100.00%)
- top chord-zone usage: 48/1157 (safe 95.85%)
- chord pads injected: 48
- style windows: w00-w00:folk_strum, w01-w05:lead_mix, w06-w06:bass_strum, w07-w07:folk_strum, w08-w18:arpeggio, w19-w19:folk_strum, w20-w22:lead_mix, w23-w26:bass_strum, w27-w27:arpeggio
- style counts: {'arpeggio': 12, 'bass_strum': 5, 'folk_strum': 3, 'lead_mix': 8, 'muted_strum': 0}
