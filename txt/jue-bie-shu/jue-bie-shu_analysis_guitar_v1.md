# Analysis (Guitar Script): jue-bie-shu.mid

## Metrics
- note_count: 1607
- duration_s: 249.2121212121212
- tempo0: 90
- tempo_events: 3
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 14.87962962962963
- bar_density_p90: 22.0
- tracks: 2
- pitch_min: 26
- pitch_max: 98

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
- playability: 1105/1105 (100.00%)
- top chord-zone usage: 27/1105 (safe 97.56%)
- chord pads injected: 27
- style windows: w00-w07:bass_strum, w08-w08:folk_strum, w09-w11:lead_mix, w12-w18:folk_strum, w19-w24:lead_mix, w25-w26:bass_strum, w27-w27:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 10, 'folk_strum': 8, 'lead_mix': 9, 'muted_strum': 0}
