# Analysis (Guitar Script): 洛克王国玩家钢琴giantmidi.mid

## Metrics
- note_count: 973
- duration_s: 178.11067708333334
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 18
- bar_density_mean: 11.447058823529412
- bar_density_p90: 18.0
- tracks: 1
- pitch_min: 34
- pitch_max: 103

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
- playability: 630/630 (100.00%)
- top chord-zone usage: 30/630 (safe 95.24%)
- chord pads injected: 30
- style windows: w00-w05:folk_strum, w06-w06:bass_strum, w07-w07:lead_mix, w08-w10:muted_strum, w11-w14:lead_mix, w15-w16:bass_strum, w17-w21:arpeggio
- style counts: {'arpeggio': 5, 'bass_strum': 3, 'folk_strum': 6, 'lead_mix': 5, 'muted_strum': 3}
