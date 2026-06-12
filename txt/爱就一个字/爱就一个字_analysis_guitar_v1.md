# Analysis (Guitar Script): 爱就一个字.mid

## Metrics
- note_count: 763
- duration_s: 129.80583640497434
- tempo0: 99
- tempo_events: 12
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 21.8
- bar_density_p90: 31.4
- tracks: 3
- pitch_min: 31
- pitch_max: 96

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
- playability: 404/404 (100.00%)
- top chord-zone usage: 3/404 (safe 99.26%)
- chord pads injected: 3
- style windows: w00-w00:arpeggio, w01-w03:bass_strum, w04-w06:lead_mix, w07-w07:bass_strum, w08-w08:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 4, 'folk_strum': 0, 'lead_mix': 3, 'muted_strum': 0}
