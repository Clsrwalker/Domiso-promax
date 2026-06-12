# Analysis (Sky MelodyLock Script v2 Safe): lemon-tree.mid

## Base
- source file: lemon-tree_domiso_script_sky_melodylock_v1.txt
- goal: keep Sky melodylock structure, but make Voice A more stable on real Sky input

## Edits
- added explicit `1=C4` to remove any base-note ambiguity
- merged short note + following short rest pairs into longer notes: 4
- replaced remaining Voice A notes under 120ms with same-length rests: 40
- remaining Voice A notes under 120ms after cleanup: 0
- Voice B and Voice C kept unchanged to preserve the accompaniment skeleton

## Expected Result
- fewer missed taps on Sky
- melody entry should be cleaner than v1
- rhythm and rollback structure stay compatible with Guangyu
