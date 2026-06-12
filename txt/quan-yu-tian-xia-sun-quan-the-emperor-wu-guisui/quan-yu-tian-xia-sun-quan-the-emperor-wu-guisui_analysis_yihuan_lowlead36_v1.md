# Analysis (Yihuan 36-Key LowLead36 Script): quan-yu-tian-xia-sun-quan-the-emperor-wu-guisui.mid

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
- yihuan_lowlead36_dense
- reason: dense piano texture -> yihuan_lowlead36_dense

## Yihuan 36-Key LowLead36 Intent
- prioritize a recognizable low-register lead over piano figurations
- preserve semitones as DoMiSo #/b tokens instead of snapping everything to white keys
- keep Voice A mostly in the low row C3-B3 (Z X C V B N M) and smooth out tiny ornament notes
- move lead notes by octave only, never by semitone, to reduce harsh high-row melody
- simplify accompaniment into sparse upper support and occasional bass anchors
- do not use semitone transposition; only octave folding is used for range
- target layout: naturals Q W E R T Y U / A S D F G H J / Z X C V B N M; semitones: Shift raises, Ctrl lowers

## Extraction Summary
- base_shift: 12
- octave_windows: w00-w47:+12
- lead_notes: 1350
- lead_from_melody_track: 1268 (93.9%)
- lead_from_top_note: 1257 (93.1%)
- fallback_lead_notes: 82
- lead_lowlead_moved: 1110
- lead_lowrow_notes: 1103
- lead_midrow_notes: 61
- lead_highrow_notes: 0
- lead_ornaments_dropped: 14
- support_notes_pruned: 3019
- chromatic_tokens: 1193
