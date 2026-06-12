# Analysis (Guitar Script): merry-christmas-mr-lawrence-ryuichi-sakamoto-merry-christmas-mrlawrence.mid

## Metrics
- note_count: 3039
- duration_s: 289.4417582417582
- tempo0: 104
- tempo_events: 3
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 19.11320754716981
- bar_density_p90: 36.0
- tracks: 2
- pitch_min: 29
- pitch_max: 97

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
- playability: 1015/1015 (100.00%)
- top chord-zone usage: 15/1015 (safe 98.52%)
- chord pads injected: 15
- style windows: w00-w02:arpeggio, w03-w04:folk_strum, w05-w05:arpeggio, w06-w11:bass_strum, w12-w12:folk_strum, w13-w13:arpeggio, w14-w17:bass_strum, w18-w19:lead_mix, w20-w26:muted_strum, w27-w27:bass_strum, w28-w29:lead_mix, w30-w30:arpeggio
- style counts: {'arpeggio': 6, 'bass_strum': 11, 'folk_strum': 3, 'lead_mix': 4, 'muted_strum': 7}
