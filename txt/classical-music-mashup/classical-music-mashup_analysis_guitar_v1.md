# Analysis (Guitar Script): classical-music-mashup.mid

## Metrics
- note_count: 3974
- duration_s: 355.5784881784882
- tempo0: 150
- tempo_events: 18
- time_sig: 4/4
- max_poly: 13
- bar_density_mean: 20.07070707070707
- bar_density_p90: 33.2
- tracks: 2
- pitch_min: 29
- pitch_max: 99

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
- playability: 2348/2348 (100.00%)
- top chord-zone usage: 44/2348 (safe 98.13%)
- chord pads injected: 44
- style windows: w00-w00:bass_strum, w01-w02:muted_strum, w03-w06:folk_strum, w07-w07:arpeggio, w08-w08:lead_mix, w09-w09:muted_strum, w10-w10:arpeggio, w11-w13:bass_strum, w14-w14:folk_strum, w15-w15:lead_mix, w16-w22:bass_strum, w23-w23:folk_strum, w24-w24:arpeggio, w25-w28:bass_strum, w29-w30:folk_strum, w31-w33:bass_strum, w34-w34:folk_strum, w35-w37:lead_mix, w38-w40:folk_strum, w41-w48:lead_mix, w49-w49:arpeggio
- style counts: {'arpeggio': 4, 'bass_strum': 18, 'folk_strum': 12, 'lead_mix': 13, 'muted_strum': 3}
