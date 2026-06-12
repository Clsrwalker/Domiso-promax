# Analysis (Guitar Script): 三有虚妄.mid

## Metrics
- note_count: 376
- duration_s: 91.89526936174494
- tempo0: 65
- tempo_events: 5
- time_sig: 3/4
- max_poly: 5
- bar_density_mean: 11.75
- bar_density_p90: 18.7
- tracks: 2
- pitch_min: 40
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
- playability: 245/245 (100.00%)
- top chord-zone usage: 11/245 (safe 95.51%)
- chord pads injected: 11
- style windows: w00-w00:folk_strum, w01-w05:bass_strum, w06-w06:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 5, 'folk_strum': 1, 'lead_mix': 0, 'muted_strum': 0}
