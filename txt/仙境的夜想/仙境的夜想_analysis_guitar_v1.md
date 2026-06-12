# Analysis (Guitar Script): 仙境的夜想.mid

## Metrics
- note_count: 522
- duration_s: 114.82931836057672
- tempo0: 137
- tempo_events: 9
- time_sig: 3/4
- max_poly: 6
- bar_density_mean: 6.0
- bar_density_p90: 9.0
- tracks: 2
- pitch_min: 34
- pitch_max: 97

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
- playability: 506/506 (100.00%)
- top chord-zone usage: 51/506 (safe 89.92%)
- chord pads injected: 51
- style windows: w00-w02:bass_strum, w03-w03:folk_strum, w04-w05:lead_mix, w06-w15:bass_strum, w16-w16:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 13, 'folk_strum': 1, 'lead_mix': 2, 'muted_strum': 0}
