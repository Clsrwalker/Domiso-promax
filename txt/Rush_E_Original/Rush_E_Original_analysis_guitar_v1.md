# Analysis (Guitar Script): Rush_E_Original.mid

## Metrics
- note_count: 19232
- duration_s: 271.95
- tempo0: 300
- tempo_events: 1
- time_sig: 4/4
- max_poly: 123
- bar_density_mean: 57.23809523809524
- bar_density_p90: 248.6
- tracks: 3
- pitch_min: 24
- pitch_max: 95

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
- playability: 2443/2443 (100.00%)
- top chord-zone usage: 78/2443 (safe 96.81%)
- chord pads injected: 77
- style windows: w00-w02:arpeggio, w03-w16:bass_strum, w17-w19:folk_strum, w20-w34:bass_strum, w35-w40:folk_strum, w41-w42:bass_strum, w43-w48:folk_strum, w49-w51:lead_mix, w52-w60:folk_strum, w61-w64:lead_mix, w65-w73:muted_strum, w74-w81:lead_mix, w82-w84:arpeggio
- style counts: {'arpeggio': 6, 'bass_strum': 31, 'folk_strum': 24, 'lead_mix': 15, 'muted_strum': 9}
