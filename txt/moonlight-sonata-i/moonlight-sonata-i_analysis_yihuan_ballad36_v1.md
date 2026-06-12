# Analysis (Yihuan 36-Key Ballad36 Script): moonlight-sonata-i.mid

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
- yihuan_ballad36_dense
- reason: dense piano texture -> yihuan_ballad36_dense

## Yihuan 36-Key Ballad36 Intent
- prioritize a singable vocal-like lead over piano figurations
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A in the middle row whenever possible and smooth out tiny ornament notes
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- simplify accompaniment into soft harmonic pads and bass anchors
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 12
- octave_windows: w00-w17:+12
- lead_notes: 807
- lead_from_melody_track: 802 (99.4%)
- lead_from_top_note: 782 (96.9%)
- fallback_lead_notes: 5
- lead_midlead_moved: 513
- lead_midrow_notes: 733
- lead_highrow_notes: 67
- lead_ornaments_dropped: 15
- support_notes_pruned: 69
- chromatic_tokens: 660
