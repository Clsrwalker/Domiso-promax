# Analysis (Guitar Script): genshin_蒙德荆夫港.mid

## Metrics
- note_count: 924
- duration_s: 277.56612318840575
- tempo0: 69
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 20.533333333333335
- bar_density_p90: 28.4
- tracks: 2
- pitch_min: 33
- pitch_max: 95

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
- playability: 367/367 (100.00%)
- top chord-zone usage: 9/367 (safe 97.55%)
- chord pads injected: 9
- style windows: w00-w03:lead_mix, w04-w04:folk_strum, w05-w05:arpeggio, w06-w11:bass_strum
- style counts: {'arpeggio': 1, 'bass_strum': 6, 'folk_strum': 1, 'lead_mix': 4, 'muted_strum': 0}
