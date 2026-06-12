# Audio To MIDI Pipeline

## Purpose

This pipeline is designed for pop-song style audio:

1. `Demucs` separates the mix into stems.
2. `basic-pitch` transcribes selected stems to MIDI with tuned presets.
3. The generated MIDIs can be merged.
4. The merged or per-stem MIDI can optionally be sent to `domiso_generate_all.py`.

The workflow is intentionally stage-based, because `mp3 -> MIDI` on CPU can take a long time.

## Main Script

`d:\domiso\tools\audio_to_midi_pipeline.py`

## Default Cache

Demucs model cache is shared here:

`d:\domiso\third_party\demucs_cache\torch`

This avoids re-downloading model weights for every new song/output folder.

## Recommended Workflow

### 1. Separate only

```powershell
python d:\domiso\tools\audio_to_midi_pipeline.py "D:\path\song.mp3" --out-dir "d:\domiso\audio_pipeline" --stage separate
```

### 2. Check progress/status

```powershell
python d:\domiso\tools\audio_to_midi_pipeline.py "D:\path\song.mp3" --out-dir "d:\domiso\audio_pipeline" --status-only
```

### 3. Transcribe vocals only

```powershell
python d:\domiso\tools\audio_to_midi_pipeline.py "D:\path\song.mp3" --out-dir "d:\domiso\audio_pipeline" --stage transcribe --transcribe-stems vocals
```

### 4. Transcribe accompaniment only

```powershell
python d:\domiso\tools\audio_to_midi_pipeline.py "D:\path\song.mp3" --out-dir "d:\domiso\audio_pipeline" --stage transcribe --transcribe-stems other
```

### 5. Merge existing stem MIDIs

```powershell
python d:\domiso\tools\audio_to_midi_pipeline.py "D:\path\song.mp3" --out-dir "d:\domiso\audio_pipeline" --stage merge --transcribe-stems vocals other
```

### 6. Send merged MIDI to DoMiSo

```powershell
python d:\domiso\tools\audio_to_midi_pipeline.py "D:\path\song.mp3" --out-dir "d:\domiso\audio_pipeline" --stage domiso --run-domiso-on merged
```

## Fast Resume Behavior

By default the script uses `--resume`.

That means:

- existing stems are reused
- existing per-stem MIDIs are reused
- existing merged MIDI is reused

If you want to force regeneration:

```powershell
python d:\domiso\tools\audio_to_midi_pipeline.py "D:\path\song.mp3" --out-dir "d:\domiso\audio_pipeline" --no-resume
```

## Current Presets

### `vocals_lead`

- keeps more vocal onset detail
- useful when the main melody is carried by singing

### `other_clean`

- cleaner accompaniment transcription
- fewer false notes than looser settings

### `other_loose`

- keeps more accompaniment detail
- may introduce more noise

### `full_mix_soft`

- fallback preset for direct full-mix transcription
- less recommended than stem-first flow

### `neuralnote_compat`

- close to NeuralNote/basic-pitch default behavior

## Report File

Every song folder writes:

`pipeline_report.json`

This report tracks:

- current overall status
- separation status
- per-stem transcription status
- merge status
- DoMiSo generation status
- produced file paths
