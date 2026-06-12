# DoMiSo Pipeline

`domiso_pipeline.py` provides a repeatable flow:

1. Analyze MIDI
2. Recommend best profile
3. Auto-convert to DoMiSo txt
4. Generate manual-arrangement analysis report
5. Compare outputs by playability

## Commands

### Analyze only

```powershell
python tools/domiso_pipeline.py analyze "C:\path\song.mid" --json
```

### Convert only

```powershell
python tools/domiso_pipeline.py convert "C:\path\song.mid" --profile auto --out-dir "d:\domiso\txt"
```

### Full pipeline (recommended)

```powershell
python tools/domiso_pipeline.py pipeline "C:\path\song.mid" --profile auto --out-dir "d:\domiso\txt" --report-dir "d:\domiso\txt"
```

### Compare two txt outputs

```powershell
python tools/domiso_pipeline.py compare "d:\domiso\txt\auto.txt" "d:\domiso\txt\manual.txt"
```

## Profiles

- `piano_solo`: melody clarity first, sparse harmony
- `pop_ballad`: balanced default
- `epic_dense`: high density material, stronger layering
- `anime_op`: fast melody-forward profile

Use `--profile auto` to let script choose based on MIDI metrics.

