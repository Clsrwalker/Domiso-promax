# Analysis (Guitar Script): merry-christmas-mr-lawrence.mid

## Metrics
- note_count: 2075
- duration_s: 312.26006191950466
- tempo0: 102
- tempo_events: 2
- time_sig: 12/8
- max_poly: 7
- bar_density_mean: 29.642857142857142
- bar_density_p90: 57.8
- tracks: 2
- pitch_min: 29
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
- playability: 820/820 (100.00%)
- top chord-zone usage: 19/820 (safe 97.68%)
- chord pads injected: 19
- style windows: w00-w02:arpeggio, w03-w04:folk_strum, w05-w05:arpeggio, w06-w15:bass_strum, w16-w17:lead_mix, w18-w25:muted_strum, w26-w26:arpeggio
- style counts: {'arpeggio': 5, 'bass_strum': 10, 'folk_strum': 2, 'lead_mix': 2, 'muted_strum': 8}
