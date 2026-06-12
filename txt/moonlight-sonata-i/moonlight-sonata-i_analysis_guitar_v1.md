# Analysis (Guitar Script): moonlight-sonata-i.mid

## Metrics
- note_count: 1164
- duration_s: 368.0027777777778
- tempo0: 45
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 16.869565217391305
- bar_density_p90: 20.0
- tracks: 2
- pitch_min: 29
- pitch_max: 87

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
- playability: 785/785 (100.00%)
- top chord-zone usage: 1/785 (safe 99.87%)
- chord pads injected: 1
- style windows: w00-w00:bass_strum, w01-w03:muted_strum, w04-w09:bass_strum, w10-w10:folk_strum, w11-w11:muted_strum, w12-w13:bass_strum, w14-w14:muted_strum, w15-w17:arpeggio
- style counts: {'arpeggio': 3, 'bass_strum': 9, 'folk_strum': 1, 'lead_mix': 0, 'muted_strum': 5}
