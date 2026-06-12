# Analysis (Guitar Script): night-dancer-imase.mid

## Metrics
- note_count: 1787
- duration_s: 210.0547201448854
- tempo0: 117
- tempo_events: 5
- time_sig: 4/4
- max_poly: 7
- bar_density_mean: 17.693069306930692
- bar_density_p90: 24.8
- tracks: 2
- pitch_min: 29
- pitch_max: 89

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
- playability: 1199/1199 (100.00%)
- top chord-zone usage: 40/1199 (safe 96.66%)
- chord pads injected: 39
- style windows: w00-w00:arpeggio, w01-w08:bass_strum, w09-w10:lead_mix, w11-w14:bass_strum, w15-w16:folk_strum, w17-w18:lead_mix, w19-w19:arpeggio, w20-w21:bass_strum, w22-w24:lead_mix, w25-w25:bass_strum
- style counts: {'arpeggio': 2, 'bass_strum': 15, 'folk_strum': 2, 'lead_mix': 7, 'muted_strum': 0}
