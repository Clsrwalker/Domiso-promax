# Analysis (Guitar Script): xenoblade-chronicles-main-theme-piano-solo.mid

## Metrics
- note_count: 719
- duration_s: 206.9454545454545
- tempo0: 55
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 15.297872340425531
- bar_density_p90: 32.0
- tracks: 2
- pitch_min: 27
- pitch_max: 94

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
- playability: 385/385 (100.00%)
- top chord-zone usage: 27/385 (safe 92.99%)
- chord pads injected: 27
- style windows: w00-w00:bass_strum, w01-w01:arpeggio, w02-w02:folk_strum, w03-w04:bass_strum, w05-w06:muted_strum, w07-w07:lead_mix, w08-w08:bass_strum, w09-w10:folk_strum, w11-w11:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 4, 'folk_strum': 3, 'lead_mix': 1, 'muted_strum': 2}
