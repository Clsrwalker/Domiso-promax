# Analysis (Guitar Script): li-kai-wo-de-yi-lai.mid

## Metrics
- note_count: 1176
- duration_s: 221.53846153846155
- tempo0: 65
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 19.6
- bar_density_p90: 30.0
- tracks: 2
- pitch_min: 34
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
- playability: 760/760 (100.00%)
- top chord-zone usage: 20/760 (safe 97.37%)
- chord pads injected: 20
- style windows: w00-w04:bass_strum, w05-w05:lead_mix, w06-w08:folk_strum, w09-w13:lead_mix, w14-w14:bass_strum, w15-w15:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 6, 'folk_strum': 3, 'lead_mix': 6, 'muted_strum': 0}
