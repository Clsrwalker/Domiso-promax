# Analysis (Guitar Script): flight-of-the-bumblebee-piano-rimsky-korsakov.mid

## Metrics
- note_count: 1133
- duration_s: 83.4375
- tempo0: 144
- tempo_events: 1
- time_sig: 2/4
- max_poly: 5
- bar_density_mean: 11.217821782178218
- bar_density_p90: 14.0
- tracks: 2
- pitch_min: 33
- pitch_max: 93

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
- playability: 344/344 (100.00%)
- top chord-zone usage: 6/344 (safe 98.26%)
- chord pads injected: 6
- style windows: w00-w00:arpeggio, w01-w02:muted_strum, w03-w05:bass_strum, w06-w07:arpeggio, w08-w10:muted_strum, w11-w11:folk_strum, w12-w12:arpeggio
- style counts: {'arpeggio': 4, 'bass_strum': 3, 'folk_strum': 1, 'lead_mix': 0, 'muted_strum': 5}
