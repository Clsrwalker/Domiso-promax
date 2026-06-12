# Analysis (Guitar Script): kokoronashi-xin-zuoshi-vocaloid.mid

## Metrics
- note_count: 1754
- duration_s: 258.12209302325584
- tempo0: 86
- tempo_events: 1
- time_sig: 4/4
- max_poly: 8
- bar_density_mean: 18.86021505376344
- bar_density_p90: 24.6
- tracks: 2
- pitch_min: 32
- pitch_max: 92

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
- playability: 1160/1160 (100.00%)
- top chord-zone usage: 25/1160 (safe 97.84%)
- chord pads injected: 25
- style windows: w00-w05:bass_strum, w06-w06:arpeggio, w07-w08:lead_mix, w09-w09:arpeggio, w10-w11:folk_strum, w12-w13:lead_mix, w14-w14:folk_strum, w15-w15:arpeggio, w16-w16:bass_strum, w17-w18:lead_mix, w19-w22:folk_strum, w23-w23:arpeggio
- style counts: {'arpeggio': 4, 'bass_strum': 7, 'folk_strum': 7, 'lead_mix': 6, 'muted_strum': 0}
