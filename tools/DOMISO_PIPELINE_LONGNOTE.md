# DoMiSo Longnote Script

`domiso_pipeline_longnote.py` is a new script (separate from existing pipeline) focused on:

- preserving sustained melody notes
- reducing ornament-like stacked overlaps
- keeping parser-safe and 21-key playable output

## Usage

### Analyze

```powershell
python tools/domiso_pipeline_longnote.py analyze "C:\path\song.mid" --json
```

### Convert (single script output)

```powershell
python tools/domiso_pipeline_longnote.py convert "C:\path\song.mid" --profile auto --out-dir "d:\domiso\txt"
```

### Full pipeline

```powershell
python tools/domiso_pipeline_longnote.py pipeline "C:\path\song.mid" --profile auto --out-dir "d:\domiso\txt" --report-dir "d:\domiso\txt"
```

## Profiles

- `longnote_solo`
- `longnote_balanced`
- `longnote_dense`

Output naming:

- `..._domiso_script_longnote_vN.txt`

Analysis naming:

- `..._analysis_longnote_vN.md`

