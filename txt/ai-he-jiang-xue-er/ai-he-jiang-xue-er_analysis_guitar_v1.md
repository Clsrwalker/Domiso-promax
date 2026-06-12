# Analysis (Guitar Script): ai-he-jiang-xue-er.mid

## Metrics
- note_count: 1017
- duration_s: 220.0
- tempo0: 72
- tempo_events: 1
- time_sig: 4/4
- max_poly: 4
- bar_density_mean: 15.646153846153846
- bar_density_p90: 19.0
- tracks: 2
- pitch_min: 39
- pitch_max: 83

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
- playability: 849/849 (100.00%)
- top chord-zone usage: 50/849 (safe 94.11%)
- chord pads injected: 50
- style windows: w00-w04:bass_strum, w05-w05:lead_mix, w06-w06:muted_strum, w07-w10:bass_strum, w11-w11:lead_mix, w12-w14:muted_strum, w15-w15:lead_mix, w16-w16:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 9, 'folk_strum': 0, 'lead_mix': 3, 'muted_strum': 4}
