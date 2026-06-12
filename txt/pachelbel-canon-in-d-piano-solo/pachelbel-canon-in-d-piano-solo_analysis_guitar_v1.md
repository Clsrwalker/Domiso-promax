# Analysis (Guitar Script): pachelbel-canon-in-d-piano-solo.mid

## Metrics
- note_count: 2210
- duration_s: 267.43035714285713
- tempo0: 70
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 28.333333333333332
- bar_density_p90: 72.0
- tracks: 2
- pitch_min: 38
- pitch_max: 90

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
- playability: 917/917 (100.00%)
- top chord-zone usage: 6/917 (safe 99.35%)
- chord pads injected: 6
- style windows: w00-w01:bass_strum, w02-w03:arpeggio, w04-w07:folk_strum, w08-w13:lead_mix, w14-w14:arpeggio, w15-w19:bass_strum
- style counts: {'arpeggio': 3, 'bass_strum': 7, 'folk_strum': 4, 'lead_mix': 6, 'muted_strum': 0}
