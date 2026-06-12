# Analysis (Guitar Script): patchwork-staccato-tsugihagisutakkato.mid

## Metrics
- note_count: 2847
- duration_s: 242.36330935251797
- tempo0: 139
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 20.19148936170213
- bar_density_p90: 29.8
- tracks: 2
- pitch_min: 36
- pitch_max: 101

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
- playability: 1532/1532 (100.00%)
- top chord-zone usage: 6/1532 (safe 99.61%)
- chord pads injected: 6
- style windows: w00-w00:arpeggio, w01-w01:bass_strum, w02-w03:folk_strum, w04-w06:bass_strum, w07-w10:folk_strum, w11-w11:bass_strum, w12-w15:lead_mix, w16-w19:folk_strum, w20-w22:arpeggio, w23-w24:lead_mix, w25-w27:muted_strum, w28-w29:bass_strum, w30-w30:muted_strum, w31-w32:lead_mix, w33-w35:arpeggio
- style counts: {'arpeggio': 7, 'bass_strum': 7, 'folk_strum': 10, 'lead_mix': 8, 'muted_strum': 4}
