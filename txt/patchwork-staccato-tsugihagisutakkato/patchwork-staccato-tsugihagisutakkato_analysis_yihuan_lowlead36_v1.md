# Analysis (Yihuan 36-Key LowLead36 Script): patchwork-staccato-tsugihagisutakkato.mid

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
- base_shift: 0
- octave_windows: w00-w35:+0
- lead_notes: 1041
- lead_from_melody_track: 962 (92.4%)
- lead_from_top_note: 982 (94.3%)
- fallback_lead_notes: 79
- lead_lowlead_moved: 766
- lead_lowrow_notes: 807
- lead_midrow_notes: 32
- lead_highrow_notes: 0
- lead_ornaments_dropped: 21
- support_notes_pruned: 983
- chromatic_tokens: 39
