# Analysis (Guitar Script): genshin无所有廊bgm.mid

## Metrics
- note_count: 886
- duration_s: 183.3556818181818
- tempo0: 110
- tempo_events: 1
- time_sig: 4/4
- max_poly: 6
- bar_density_mean: 11.35897435897436
- bar_density_p90: 16.1
- tracks: 2
- pitch_min: 42
- pitch_max: 92

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
- playability: 800/800 (100.00%)
- top chord-zone usage: 43/800 (safe 94.62%)
- chord pads injected: 43
- style windows: w00-w02:arpeggio, w03-w03:bass_strum, w04-w05:muted_strum, w06-w07:bass_strum, w08-w09:lead_mix, w10-w10:bass_strum, w11-w14:folk_strum, w15-w16:lead_mix, w17-w17:muted_strum, w18-w19:bass_strum
- style counts: {'arpeggio': 3, 'bass_strum': 6, 'folk_strum': 4, 'lead_mix': 4, 'muted_strum': 3}
