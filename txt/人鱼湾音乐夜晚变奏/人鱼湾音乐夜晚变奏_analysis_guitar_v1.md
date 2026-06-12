# Analysis (Guitar Script): 人鱼湾音乐夜晚变奏.mid

## Metrics
- note_count: 359
- duration_s: 103.04086538461539
- tempo0: 91
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 8.975
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 41
- pitch_max: 96

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
- playability: 292/292 (100.00%)
- top chord-zone usage: 37/292 (safe 87.33%)
- chord pads injected: 36
- style windows: w00-w00:bass_strum, w01-w02:muted_strum, w03-w03:lead_mix, w04-w04:bass_strum, w05-w05:arpeggio, w06-w06:folk_strum, w07-w07:lead_mix, w08-w08:bass_strum, w09-w09:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 3, 'folk_strum': 1, 'lead_mix': 2, 'muted_strum': 2}
