# Manual Analysis: what-a-delightful-scenery-genshin-impact-chenyu-vale-yilong-wharf-yuxi-wang-hoyo-mix.mid

## Multi-instrument Melody Handling
- This MIDI has many layered tracks; single fixed melody-track fails in several sections.
- Melody track is selected per 4-bar window with continuity penalty to avoid random switching.
- Selected windows: w00-w00:t13, w01-w06:t0, w07-w10:t17, w11-w19:t0

## Arrangement
- Voice A: contour-first melody extraction from section-selected melody track, with fallback to local high line.
- Voice B: strong/eighth beat support tones only (reduced clutter).
- Voice C: bass anchors on beat/eighth from low/bass tracks.

## Output
- Manual txt: what-a-delightful-scenery-genshin-impact-chenyu-vale-yilong-wharf-yuxi-wang-hoyo-mix_domiso_manual_v2.txt
- Parser/lint: passed.