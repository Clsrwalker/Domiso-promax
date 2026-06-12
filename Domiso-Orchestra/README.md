# Domiso Orchestra

Domiso Orchestra is a LAN room system for multi-computer Domiso/Sky ensemble playback.

It does not stream every key press over the network. The Conductor only manages the room, track assignment, loading, ready state, and a future `START` time. Each Player Client receives its assigned tracks and performs deterministic local playback.

## Architecture

```text
Conductor PC
  Web UI + FastAPI server
  Project JSON upload
  Multi TXT import
  Track assignment
  Ready / Start / Pause / Resume / Stop

Player PC-A
  WebSocket client
  Assigned tracks
  Local parser/playback

Player PC-B / PC-C / ...
  Same client, different assigned tracks
```

## Install

```powershell
cd D:\domiso\Domiso-Orchestra
python -m pip install -r requirements.txt
```

## Start the Conductor

```powershell
cd D:\domiso\Domiso-Orchestra
python -m domiso_orchestra.conductor --host 0.0.0.0 --port 8765
```

Open the control UI on the Conductor PC:

```text
http://127.0.0.1:8765
```

Other computers on the same LAN should open:

```text
http://CONDUCTOR_IP:8765
```

## Conductor UI

The UI supports three project inputs:

- JSON project: choose a `.json` file, click `Read JSON File`, then `Upload JSON`.
- Domiso TXT/DMS tracks: choose multiple `.txt` or `.dms` files, select `sky15` or `domiso36`, choose pitch naming, then click `Build Project From TXT`.
- MIDI project: choose a `.mid` or `.midi` file, select a layout, then click `Build Project From MIDI`.

Each TXT file becomes one independent track. Assign tracks to connected clients in the Tracks table, then click `Prepare / Load Tracks`.
Each `.dms` file is decrypted server-side and converted into the same internal event format.
Each MIDI track with playable notes becomes one project track.

The room status panel shows `EMPTY`, `PROJECT_LOADED`, `LOADING`, `ARMED`, `PLAYING`, `PAUSED`, `FINISHED`, or `STOPPED`. When a future start time is scheduled, the UI shows the remaining countdown.
Use `Download Current JSON` to export the normalized multi-track project after importing TXT/DMS/MIDI.
Use `Start pos ms` or the seek slider to start all assigned clients from the same position in the song. `Use Progress` copies the furthest current client progress into that field.

Pitch naming:

- `standard C4=60`: use this for the generated Sky/Domiso TXT files from this repo's Python tools.
- `domiso C5=60`: use this for original Domiso sheets that follow Domiso's bundled `NoteData` naming.

Playback profile values mirror Domiso's Windows auto-play behavior:

- `Speed %`: scales the generated action timeline.
- `Hold min ms`: notes shorter than this are sent as short taps.
- `Same key gap ms`: same-key notes starting too close together are merged.
- `Tap ms`: key hold time for short taps.
- `Release early ms`: long notes release this many milliseconds before their written duration ends.

The Clients table shows:

- `State`: CONNECTED, LOADED, READY, ARMED, PLAYING, PAUSED, FINISHED, ERROR, or DISCONNECTED.
- `Delay ms`: per-client manual timing offset.
- `RTT`: current and best clock sync round-trip time.
- `Offset`: estimated server/client monotonic clock offset.
- `Progress`: local playback position for that client.
- `Error`: last client-side error.

Use the per-client `Ready` button when a Player Client is started with `--manual-ready`.
Use the per-client `Pulse` button to send a short test pulse to that computer for focus and delay calibration.

When the browser page is focused, playback hotkeys mirror Domiso's local controls:

- `F7`: Pause
- `F8`: Stop
- `F9`: Start from beginning after the normal countdown
- `F10`: Resume

## Start Player Clients

Dry-run mode is safe and prints no keys by default:

```powershell
cd D:\domiso\Domiso-Orchestra
python -m domiso_orchestra.player_client --server ws://CONDUCTOR_IP:8765/ws/player --client-id PC-A --backend dry-run
python -m domiso_orchestra.player_client --server ws://CONDUCTOR_IP:8765/ws/player --client-id PC-B --backend dry-run
```

Manual ready mode:

```powershell
python -m domiso_orchestra.player_client --server ws://CONDUCTOR_IP:8765/ws/player --client-id PC-C --backend dry-run --manual-ready
```

Real Windows key injection:

```powershell
python -m domiso_orchestra.player_client --server ws://CONDUCTOR_IP:8765/ws/player --client-id PC-A --backend windows --window-title "Sky"
```

`windows` uses the Domiso-compatible event-style keyboard backend. `windows-input` is also available as a SendInput fallback if a specific game accepts that better.

If `--window-title` is provided, the client tries to activate the first visible Windows window whose title contains that text before Start or Pulse. Without it, keep the target game window focused before pressing Start.

List matching Windows titles:

```powershell
python -m domiso_orchestra.player_client --list-windows --window-title "Sky"
```

Send a local test pulse without connecting to the Conductor:

```powershell
python -m domiso_orchestra.player_client --local-pulse --backend windows --window-title "Sky" --local-pulse-key y
```

Client settings are saved by default to:

```text
%USERPROFILE%\.domiso-orchestra\CLIENT_ID.json
```

The saved config includes `clientId`, `layout`, `backend`, `inputDelayOffsetMs`, manual ready mode, and `windowTitle`. Use an explicit config path when needed:

```powershell
python -m domiso_orchestra.player_client --config D:\domiso\pc-a.client.json
```

Use `--no-save-config` for temporary test clients.

## Delay Calibration

Each client has `inputDelayOffsetMs`.

- `-20` means this client plays 20 ms earlier.
- `+10` means this client plays 10 ms later.

Set it in the Conductor UI per client.

The client applies this delay locally when converting the shared `startAtServerTimeMs` into its own monotonic clock. That keeps playback deterministic even if Wi-Fi latency varies after Start.

## Project Format

```json
{
  "schemaVersion": "domiso-orchestra.project.v1",
  "songId": "canon_multi_track",
  "title": "Canon Multi Track",
  "playbackProfile": {
    "speedPercent": 95,
    "holdMinMs": 150,
    "sameKeyMinGapMs": 110,
    "tapPressMs": 14,
    "longNoteReleaseEarlyMs": 80
  },
  "tracks": [
    {
      "id": "track_1",
      "name": "Main Melody",
      "layout": "sky15",
      "events": [
        {"timeMs": 0, "durationMs": 500, "keys": ["y"]},
        {"timeMs": 500, "durationMs": 500, "keys": ["u", "i"]}
      ]
    }
  ]
}
```

Any track can be assigned to any connected PC. Multiple tracks can be assigned to the same PC.

## Convert Domiso TXT Tracks Into a Project

```powershell
python -m domiso_orchestra.project_tool from-domiso output.project.json A.txt B.txt --layout sky15 --pitch-naming standard --song-id my_song --title "My Song"
```

For original Domiso bundled sheets, use:

```powershell
python -m domiso_orchestra.project_tool from-domiso output.project.json old_domiso_sheet.txt --layout domiso36 --pitch-naming domiso
```

Then upload `output.project.json` in the Conductor UI.

You can also skip this command and import multiple `.txt` files directly in the Conductor UI.
The same command and UI also accept Domiso `.dms` files.

## Convert MIDI Into a Project

```powershell
python -m domiso_orchestra.project_tool from-midi output.project.json song.mid --layout domiso36 --song-id my_song --title "My Song"
```

The built-in MIDI importer does not require `mido`. It reads Standard MIDI files, converts note events to internal project events, and skips notes that do not fit the selected layout.

## Room Flow

1. Start Conductor.
2. Start one Player Client on each performance computer.
3. Upload a project JSON.
4. Assign each track to a client.
5. Click `Prepare / Load Tracks`.
6. Wait until clients show `READY`.
7. Click `Start +5s`.

During playback you can use `Pause`, `Resume`, or `Stop`. `Stop` releases all held keys on each client.
For rehearsals, set `Start pos ms` before Start to begin from the middle of the project. Long notes already active at that position are pressed locally at the scheduled start time.

## Verify

```powershell
cd D:\domiso\Domiso-Orchestra
python verify_orchestra.py
python smoke_lan.py
```

`verify_orchestra.py` checks Domiso parsing, pitch naming modes, key mapping, project conversion, and dry-run playback planning. `smoke_lan.py` starts a local Conductor plus three dry-run clients, imports TXT tracks, uploads a four-track sample project, assigns tracks across PC-A/PC-B/PC-C, verifies manual Ready, starts, pauses, resumes, and waits for playback to finish.
