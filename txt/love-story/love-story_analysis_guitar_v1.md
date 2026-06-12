# Analysis (Guitar Script): love-story.mid

## Metrics
- note_count: 793
- duration_s: 104.0
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 15.25
- bar_density_p90: 26.1
- tracks: 2
- pitch_min: 31
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
- playability: 541/541 (100.00%)
- top chord-zone usage: 22/541 (safe 95.93%)
- chord pads injected: 22
- style windows: w00-w02:bass_strum, w03-w07:lead_mix, w08-w12:bass_strum, w13-w13:arpeggio
- style counts: {'arpeggio': 1, 'bass_strum': 8, 'folk_strum': 0, 'lead_mix': 5, 'muted_strum': 0}
