# Analysis (Guitar Script): 能不能给我一首歌的时间-zhou-jie-lun.mid

## Metrics
- note_count: 1734
- duration_s: 248.94915254237287
- tempo0: 59
- tempo_events: 1
- time_sig: 1/4
- max_poly: 6
- bar_density_mean: 7.1652892561983474
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 23
- pitch_max: 87

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
- playability: 843/843 (100.00%)
- top chord-zone usage: 7/843 (safe 99.17%)
- chord pads injected: 7
- style windows: w00-w07:bass_strum, w08-w09:folk_strum, w10-w10:muted_strum, w11-w11:bass_strum, w12-w14:folk_strum, w15-w15:bass_strum
- style counts: {'arpeggio': 0, 'bass_strum': 10, 'folk_strum': 5, 'lead_mix': 0, 'muted_strum': 1}
