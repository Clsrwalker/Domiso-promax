# Analysis (Yihuan 36-Key Ballad36 Script): quan-yu-tian-xia-sun-quan-the-emperor-wu-guisui.mid

## Metrics
- note_count: 5421
- duration_s: 246.48716216216218
- tempo0: 185
- tempo_events: 1
- time_sig: 4/4
- max_poly: 9
- bar_density_mean: 28.682539682539684
- bar_density_p90: 40.0
- tracks: 2
- pitch_min: 25
- pitch_max: 97

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
- octave_windows: w00-w47:+12
- lead_notes: 1347
- lead_from_melody_track: 1268 (94.1%)
- lead_from_top_note: 1047 (77.7%)
- fallback_lead_notes: 79
- lead_midlead_moved: 831
- lead_midrow_notes: 1059
- lead_highrow_notes: 83
- lead_ornaments_dropped: 4
- support_notes_pruned: 100
- chromatic_tokens: 1905
