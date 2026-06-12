# Analysis (Guitar Script): runaway-aurora.mid

## Metrics
- note_count: 1802
- duration_s: 323.90643236074277
- tempo0: 58
- tempo_events: 2
- time_sig: 6/8
- max_poly: 7
- bar_density_mean: 15.669565217391304
- bar_density_p90: 26.8
- tracks: 2
- pitch_min: 28
- pitch_max: 99

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
- playability: 933/933 (100.00%)
- top chord-zone usage: 32/933 (safe 96.57%)
- chord pads injected: 32
- style windows: w00-w02:bass_strum, w03-w03:arpeggio, w04-w07:folk_strum, w08-w11:lead_mix, w12-w12:muted_strum, w13-w15:bass_strum, w16-w16:folk_strum, w17-w17:lead_mix, w18-w18:muted_strum, w19-w19:folk_strum, w20-w21:bass_strum
- style counts: {'arpeggio': 1, 'bass_strum': 8, 'folk_strum': 6, 'lead_mix': 5, 'muted_strum': 2}
