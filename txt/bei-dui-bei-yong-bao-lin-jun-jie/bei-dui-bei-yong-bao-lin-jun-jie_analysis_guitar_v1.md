# Analysis (Guitar Script): bei-dui-bei-yong-bao-lin-jun-jie.mid

## Metrics
- note_count: 1166
- duration_s: 228.89944229171942
- tempo0: 130
- tempo_events: 10
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 9.636363636363637
- bar_density_p90: 14.0
- tracks: 2
- pitch_min: 22
- pitch_max: 82

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
- playability: 1159/1159 (100.00%)
- top chord-zone usage: 109/1159 (safe 90.60%)
- chord pads injected: 109
- style windows: w00-w00:muted_strum, w01-w10:bass_strum, w11-w13:muted_strum, w14-w18:lead_mix, w19-w20:muted_strum, w21-w21:lead_mix, w22-w23:bass_strum, w24-w24:folk_strum, w25-w25:lead_mix, w26-w26:arpeggio, w27-w29:bass_strum, w30-w30:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 15, 'folk_strum': 1, 'lead_mix': 7, 'muted_strum': 6}
