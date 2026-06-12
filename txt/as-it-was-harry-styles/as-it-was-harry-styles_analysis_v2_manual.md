# Manual Analysis: as-it-was-harry-styles.mid

## Track Findings
- Track0: high register single-line melody (range 64-81, ~350 notes).
- Track1: accompaniment/rhythm bed (range 40-57, ~679 notes).
- Tempo: 174 BPM, Time signature: 4/4, stable tempo map.

## Arrangement Strategy (Manual)
- Voice A: use Track0 as primary melody only (monophonic contour first).
- Voice B: extract upper rhythmic support from accompaniment offbeats.
- Voice C: bass pulse from low accompaniment anchors.
- Ornament policy: source-derived only, no synthetic decorative runs.
- Transpose policy: single global shift to maximize playable mapping and preserve line.

## Output and Validation
- Manual output: as-it-was-harry-styles_domiso_arranged_v4_dense3layer.txt
- Parser compatibility: passed (3 voices + 2 rollback + no accidental tokens).
- Playability simulation: 100%.

## Auto vs Manual (Current)
- Auto v1 has denser A-layer and larger jump profile.
- Manual v4 reduces A-layer jump rate and keeps clearer singable contour.

## Script Library Enrichment Candidates
- Add profile rule: if one track is high monophonic melody and another is low accompaniment, force melody-track-first A extraction.
- Add profile rule: for fast 4/4 pop songs, prefer offbeat B support + beat-anchored C pulse.
- Add scoring feature: penalize A-layer large leaps (>=6 scale steps) during profile selection.
