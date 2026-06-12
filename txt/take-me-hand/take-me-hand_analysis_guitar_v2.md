# Analysis (Guitar Script): take-me-hand.mid

## Metrics
- note_count: 1477
- duration_s: 258.64453125
- tempo0: 128
- tempo_events: 1
- time_sig: 4/4
- max_poly: 5
- bar_density_mean: 10.781021897810218
- bar_density_p90: 15.0
- tracks: 2
- pitch_min: 43
- pitch_max: 81

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
- playability: 1603/1603 (100.00%)
- top chord-zone usage: 124/1603 (safe 92.26%)
- chord pads injected: 122
- style windows: w00-w01:arpeggio, w02-w07:bass_strum, w08-w12:folk_strum, w13-w14:lead_mix, w15-w15:arpeggio, w16-w16:folk_strum, w17-w19:bass_strum, w20-w20:muted_strum, w21-w23:lead_mix, w24-w27:bass_strum, w28-w28:muted_strum, w29-w31:lead_mix, w32-w32:muted_strum, w33-w33:folk_strum, w34-w34:arpeggio
- style counts: {'arpeggio': 4, 'bass_strum': 13, 'folk_strum': 7, 'lead_mix': 8, 'muted_strum': 3}
