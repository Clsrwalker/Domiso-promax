# Analysis (Literal Transcription Script): 洛克王国玩家钢琴giantmidi.mid

## Metrics
- note_count: 973
- duration_s: 178.11067708333334
- tempo0: 120
- tempo_events: 1
- time_sig: 4/4
- max_poly: 18
- bar_density_mean: 11.447058823529412
- bar_density_p90: 18.0
- tracks: 1
- pitch_min: 34
- pitch_max: 103
- single_note_track: True
- out_of_range_ratio: 0.2292
- black_key_ratio: 0.2497
- start_dev_median_ticks: 23.0
- start_dev_p90_ticks: 43.0

## Recommended Profile
- literal_transcription_dense
- reason: single-track dense piano transcription -> literal_transcription_dense

## Transcription Intent
- treat source as a single-track piano transcription rather than a clean arranged MIDI
- keep a singable top contour, but preserve beat-anchored bass and harmonic body where possible
- collapse same-pitch duplicates caused by transcription + playable snapping before serialization

## Extraction Summary
- base_shift: -5
- dynamic_windows: w00-w07:-5, w08-w12:-3, w13-w21:-7
- collapsed_same_pitch_onsets: 38
- lead_notes: 516
- lead_from_top_note: 503 (97.5%)
- lead_from_rank1_or_2: 13 (2.5%)
- fallback_lead_notes: 0
- companion_notes: 84
- companion_on_strong: 32
- companion_on_offbeat: 52
- support_notes_pruned: 57
