# Analysis (Guitar Script): 樱花草.mid

## Metrics
- note_count: 1110
- duration_s: 195.12797619047618
- tempo0: 147
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 9.40677966101695
- bar_density_p90: 12.0
- tracks: 2
- pitch_min: 26
- pitch_max: 83

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
- playability: 756/756 (100.00%)
- top chord-zone usage: 69/756 (safe 90.87%)
- chord pads injected: 68
- style windows: w00-w06:bass_strum, w07-w07:arpeggio, w08-w08:folk_strum, w09-w09:muted_strum, w10-w13:lead_mix, w14-w21:bass_strum, w22-w22:folk_strum, w23-w26:lead_mix, w27-w27:folk_strum, w28-w28:bass_strum, w29-w29:arpeggio
- style counts: {'arpeggio': 2, 'bass_strum': 16, 'folk_strum': 3, 'lead_mix': 8, 'muted_strum': 1}
