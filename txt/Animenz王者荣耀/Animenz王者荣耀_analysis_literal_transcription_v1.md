# Analysis (Literal Transcription Script): Animenz王者荣耀.mid

## Metrics
- note_count: 5301
- duration_s: 506.0611979166667
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 23
- bar_density_mean: 21.204
- bar_density_p90: 32.0
- tracks: 1
- pitch_min: 26
- pitch_max: 104
- single_note_track: True
- out_of_range_ratio: 0.2741
- black_key_ratio: 0.3978
- start_dev_median_ticks: 24.0
- start_dev_p90_ticks: 43.0

## Recommended Profile
- literal_transcription_dense
- reason: single-track dense piano transcription -> literal_transcription_dense

## Transcription Intent
- treat source as a single-track piano transcription rather than a clean arranged MIDI
- keep a singable top contour, but preserve beat-anchored bass and harmonic body where possible
- collapse same-pitch duplicates caused by transcription + playable snapping before serialization

## Extraction Summary
- base_shift: 2
- dynamic_windows: w00-w13:+2, w14-w31:+1, w32-w62:+2
- collapsed_same_pitch_onsets: 538
- lead_notes: 2690
- lead_from_top_note: 2630 (97.8%)
- lead_from_rank1_or_2: 60 (2.2%)
- fallback_lead_notes: 0
- companion_notes: 665
- companion_on_strong: 224
- companion_on_offbeat: 441
- support_notes_pruned: 173
