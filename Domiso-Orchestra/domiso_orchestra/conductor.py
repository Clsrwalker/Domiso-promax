from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse

from .midi_import import midi_base64_to_project
from .playback import actions_duration_ms, build_actions
from .project import normalize_project, project_from_domiso_tracks, subset_project


def server_time_ms() -> int:
    return int(time.monotonic() * 1000)


def playback_duration_ms(project: Dict[str, object], tracks: Optional[List[Dict[str, object]]] = None) -> int:
    selected_tracks = tracks if tracks is not None else [
        t for t in project.get("tracks", []) if isinstance(t, dict)
    ]
    return actions_duration_ms(build_actions(selected_tracks, project.get("playbackProfile")))


@dataclass
class ClientSession:
    client_id: str
    name: str
    layout: str = "sky15"
    window_title: str = ""
    state: str = "CONNECTED"
    input_delay_offset_ms: int = 0
    sync_rtt_ms: float = 0.0
    best_sync_rtt_ms: float = 0.0
    clock_offset_ms: float = 0.0
    progress_ms: int = 0
    duration_ms: int = 0
    connected_at_ms: int = field(default_factory=server_time_ms)
    last_seen_ms: int = field(default_factory=server_time_ms)
    loaded_tracks: List[str] = field(default_factory=list)
    error: str = ""
    websocket: Optional[WebSocket] = field(default=None, repr=False, compare=False)

    def public(self) -> Dict[str, object]:
        return {
            "client_id": self.client_id,
            "name": self.name,
            "layout": self.layout,
            "windowTitle": self.window_title,
            "state": self.state,
            "input_delay_offset_ms": self.input_delay_offset_ms,
            "syncRttMs": self.sync_rtt_ms,
            "bestSyncRttMs": self.best_sync_rtt_ms,
            "clockOffsetMs": self.clock_offset_ms,
            "progressMs": self.progress_ms,
            "durationMs": self.duration_ms,
            "connected_at_ms": self.connected_at_ms,
            "last_seen_ms": self.last_seen_ms,
            "loaded_tracks": list(self.loaded_tracks),
            "error": self.error,
            "online": self.websocket is not None,
        }


class OrchestraRoom:
    def __init__(self) -> None:
        self.clients: Dict[str, ClientSession] = {}
        self.project: Optional[Dict[str, object]] = None
        self.assignments: Dict[str, str] = {}
        self.room_state = "EMPTY"
        self.scheduled_start_at_ms: Optional[int] = None
        self.scheduled_start_position_ms: int = 0
        self.lock = asyncio.Lock()

    async def public_state(self) -> Dict[str, object]:
        async with self.lock:
            now = server_time_ms()
            assigned_clients = {cid for cid in self.assignments.values() if cid}
            if self.room_state == "ARMED" and self.scheduled_start_at_ms and now >= self.scheduled_start_at_ms:
                self.room_state = "PLAYING"
            if assigned_clients:
                assigned_states = [
                    self.clients[cid].state for cid in assigned_clients if self.clients.get(cid)
                ]
                if (
                    self.room_state in {"LOADING", "PROJECT_LOADED", "STOPPED", "FINISHED"}
                    and assigned_states
                    and all(state == "READY" for state in assigned_states)
                ):
                    self.room_state = "READY"
                    self.scheduled_start_at_ms = None
                    self.scheduled_start_position_ms = 0
                if any(state == "PLAYING" for state in assigned_states) and self.room_state != "PAUSED":
                    self.room_state = "PLAYING"
                if assigned_states and all(state == "FINISHED" for state in assigned_states):
                    self.room_state = "FINISHED"
                    self.scheduled_start_at_ms = None
                    self.scheduled_start_position_ms = 0
            tracks = []
            project_duration_ms = 0
            if self.project:
                project_duration_ms = playback_duration_ms(self.project)
                tracks = [
                    {
                        "id": t["id"],
                        "name": t.get("name", t["id"]),
                        "layout": t.get("layout", "sky15"),
                        "events": len(t.get("events", [])),
                        "durationMs": playback_duration_ms(self.project, [t]),
                        "assignedTo": self.assignments.get(str(t["id"]), ""),
                    }
                    for t in self.project.get("tracks", [])
                    if isinstance(t, dict)
                ]
            return {
                "serverTimeMs": now,
                "roomState": self.room_state,
                "scheduledStartAtServerTimeMs": self.scheduled_start_at_ms,
                "scheduledStartPositionMs": self.scheduled_start_position_ms,
                "project": {
                    "songId": self.project.get("songId"),
                    "title": self.project.get("title"),
                    "durationMs": project_duration_ms,
                    "playbackProfile": self.project.get("playbackProfile"),
                    "tracks": tracks,
                }
                if self.project
                else None,
                "assignments": dict(self.assignments),
                "clients": [c.public() for c in sorted(self.clients.values(), key=lambda c: c.client_id)],
            }

    async def register(self, ws: WebSocket, hello: Dict[str, object]) -> ClientSession:
        client_id = str(hello.get("clientId") or "").strip()
        if not client_id:
            raise ValueError("HELLO.clientId is required")
        async with self.lock:
            session = self.clients.get(client_id) or ClientSession(
                client_id=client_id,
                name=str(hello.get("name") or client_id),
            )
            session.websocket = ws
            session.name = str(hello.get("name") or session.name or client_id)
            session.layout = str(hello.get("layout") or session.layout or "sky15")
            session.window_title = str(hello.get("windowTitle") or session.window_title or "")
            session.state = "CONNECTED"
            session.input_delay_offset_ms = int(hello.get("inputDelayOffsetMs") or session.input_delay_offset_ms)
            session.connected_at_ms = server_time_ms()
            session.last_seen_ms = session.connected_at_ms
            session.error = ""
            self.clients[client_id] = session
            return session

    async def update_client(self, client_id: str, payload: Dict[str, object]) -> None:
        async with self.lock:
            session = self.clients.get(client_id)
            if not session:
                return
            session.last_seen_ms = server_time_ms()
            if "state" in payload:
                session.state = str(payload["state"])
            if "loadedTracks" in payload and isinstance(payload["loadedTracks"], list):
                session.loaded_tracks = [str(x) for x in payload["loadedTracks"]]
            if "error" in payload:
                session.error = str(payload["error"])
                if session.error:
                    session.state = "ERROR"
            if "inputDelayOffsetMs" in payload:
                session.input_delay_offset_ms = int(payload["inputDelayOffsetMs"])
            if "windowTitle" in payload:
                session.window_title = str(payload["windowTitle"] or "")
            if "syncRttMs" in payload:
                session.sync_rtt_ms = float(payload["syncRttMs"])
            if "bestSyncRttMs" in payload:
                session.best_sync_rtt_ms = float(payload["bestSyncRttMs"])
            if "clockOffsetMs" in payload:
                session.clock_offset_ms = float(payload["clockOffsetMs"])
            if "progressMs" in payload:
                session.progress_ms = int(payload["progressMs"])
            if "durationMs" in payload:
                session.duration_ms = int(payload["durationMs"])

    async def disconnect(self, client_id: str, ws: WebSocket) -> None:
        async with self.lock:
            session = self.clients.get(client_id)
            if session and session.websocket is ws:
                session.websocket = None
                session.state = "DISCONNECTED"
                session.last_seen_ms = server_time_ms()

    async def send_command(self, client_id: str, command: Dict[str, object]) -> None:
        async with self.lock:
            session = self.clients.get(client_id)
            ws = session.websocket if session else None
        if not ws:
            raise RuntimeError(f"client not connected: {client_id}")
        try:
            await asyncio.wait_for(ws.send_json(command), timeout=2.0)
        except Exception as exc:
            async with self.lock:
                session = self.clients.get(client_id)
                if session:
                    session.state = "ERROR"
                    session.error = f"send command failed: {exc}"
            raise RuntimeError(f"send command failed for {client_id}: {exc}") from exc

    async def assigned_client_ids(self) -> List[str]:
        async with self.lock:
            return sorted(set(self.assignments.values()))

    async def assigned_tracks_for(self, client_id: str) -> List[str]:
        async with self.lock:
            return [track_id for track_id, assigned in self.assignments.items() if assigned == client_id]


room = OrchestraRoom()
app = FastAPI(title="Domiso Orchestra Conductor", version="0.1.0")


INDEX_HTML = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Domiso Orchestra Conductor</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 24px; color: #1d232a; background: #f7f8fa; }
    h1 { font-size: 24px; }
    h2 { font-size: 18px; margin-top: 24px; }
    textarea { width: 100%; min-height: 180px; font-family: ui-monospace, monospace; }
    table { border-collapse: collapse; width: 100%; background: white; }
    th, td { border: 1px solid #d8dde3; padding: 8px; text-align: left; }
    button, select, input { padding: 7px 10px; margin: 4px 4px 4px 0; }
    .row { display: flex; gap: 16px; align-items: flex-start; }
    .panel { background: white; border: 1px solid #d8dde3; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
    .small { color: #5b6470; font-size: 12px; }
    .state { font-weight: 600; }
    .toolbar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .field { display: inline-flex; align-items: center; gap: 6px; margin-right: 12px; }
    .field input[type="text"] { width: 170px; }
    .field input[type="number"] { width: 90px; }
    input[type="file"] { max-width: 320px; }
    progress { width: 130px; height: 12px; }
    .error { color: #b42318; max-width: 220px; overflow-wrap: anywhere; }
  </style>
</head>
<body>
    <h1>Domiso Orchestra Conductor</h1>
  <div class="panel">
    <span class="state" id="roomState">EMPTY</span>
    <span id="countdown" class="small"></span>
  </div>
  <div class="panel">
    <div class="toolbar">
      <button onclick="loadSample()">Load Sample</button>
      <input id="projectFile" type="file" accept=".json,application/json">
      <button onclick="loadProjectFile()">Read JSON File</button>
      <button onclick="uploadProject()">Upload JSON</button>
      <button onclick="downloadCurrentProject()">Download Current JSON</button>
      <button onclick="prepare()">Prepare / Load Tracks</button>
      <label class="field">Start pos ms <input id="startPositionMs" type="number" value="0" min="0"></label>
      <input id="seekPosition" type="range" min="0" max="0" value="0" step="10" oninput="setStartPosition(this.value)">
      <button onclick="useCurrentProgress()">Use Progress</button>
      <button onclick="start()">Start +5s</button>
      <button onclick="pause()">Pause</button>
      <button onclick="resume()">Resume</button>
      <button onclick="stop()">Stop</button>
    </div>
    <span id="status" class="small"></span>
    <textarea id="projectJson" spellcheck="false"></textarea>
  </div>
  <div class="panel">
    <h2>Import Domiso TXT / DMS Tracks</h2>
    <label class="field">Song ID <input id="domisoSongId" type="text" value="domiso_project"></label>
    <label class="field">Title <input id="domisoTitle" type="text" value="Domiso Project"></label>
    <label class="field">Layout
      <select id="domisoLayout">
        <option value="sky15">sky15</option>
        <option value="domiso36">domiso36</option>
      </select>
    </label>
    <label class="field">Pitch names
      <select id="domisoPitchNaming">
        <option value="standard">standard C4=60</option>
        <option value="domiso">domiso C5=60</option>
      </select>
    </label>
    <input id="domisoFiles" type="file" multiple accept=".txt,.dms,text/plain">
    <button onclick="importDomisoFiles()">Build Project From TXT/DMS</button>
    <div>
      <label class="field">Speed % <input id="profileSpeed" type="number" value="95" min="1" max="300"></label>
      <label class="field">Hold min ms <input id="profileHoldMin" type="number" value="150" min="1"></label>
      <label class="field">Same key gap ms <input id="profileSameKeyGap" type="number" value="110" min="0"></label>
      <label class="field">Tap ms <input id="profileTapPress" type="number" value="14" min="1"></label>
      <label class="field">Release early ms <input id="profileReleaseEarly" type="number" value="80" min="0"></label>
    </div>
  </div>
  <div class="panel">
    <h2>Import MIDI</h2>
    <label class="field">Song ID <input id="midiSongId" type="text" value="midi_project"></label>
    <label class="field">Title <input id="midiTitle" type="text" value="MIDI Project"></label>
    <label class="field">Layout
      <select id="midiLayout">
        <option value="domiso36">domiso36</option>
        <option value="sky15">sky15</option>
      </select>
    </label>
    <input id="midiFile" type="file" accept=".mid,.midi,audio/midi">
    <button onclick="importMidiFile()">Build Project From MIDI</button>
  </div>
  <div class="row">
    <div class="panel" style="flex: 1">
      <h2>Clients</h2>
      <table><thead><tr><th>ID</th><th>Name</th><th>State</th><th>Layout</th><th>Window</th><th>Delay ms</th><th>RTT</th><th>Offset</th><th>Progress</th><th>Tracks</th><th>Action</th><th>Error</th></tr></thead><tbody id="clients"></tbody></table>
    </div>
    <div class="panel" style="flex: 1">
      <h2>Tracks</h2>
      <table><thead><tr><th>Track</th><th>Events</th><th>Assign To</th></tr></thead><tbody id="tracks"></tbody></table>
    </div>
  </div>
<script>
const sample = {
  schemaVersion: "domiso-orchestra.project.v1",
  songId: "sample_twinkle",
  title: "Sample Two Track",
  playbackProfile: {
    speedPercent: 95,
    holdMinMs: 150,
    sameKeyMinGapMs: 110,
    tapPressMs: 14,
    longNoteReleaseEarlyMs: 80
  },
  tracks: [
    {id: "track_1", name: "Melody", layout: "sky15", events: [
      {timeMs: 0, durationMs: 300, keys: ["y"]},
      {timeMs: 500, durationMs: 300, keys: ["y"]},
      {timeMs: 1000, durationMs: 300, keys: ["p"]},
      {timeMs: 1500, durationMs: 300, keys: ["p"]}
    ]},
    {id: "track_2", name: "Harmony", layout: "sky15", events: [
      {timeMs: 0, durationMs: 900, keys: ["y", "p"]},
      {timeMs: 1000, durationMs: 900, keys: ["u", "h"]}
    ]}
  ]
};
let state = null;
function setStatus(msg) { document.getElementById("status").textContent = msg; }
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[ch]));
}
function fmtNumber(value, digits = 0) {
  const n = Number(value || 0);
  return Number.isFinite(n) ? n.toFixed(digits) : "-";
}
function progressText(c) {
  const progress = Number(c.progressMs || 0);
  const duration = Number(c.durationMs || 0);
  return `${(progress / 1000).toFixed(1)} / ${(duration / 1000).toFixed(1)} s`;
}
function projectDuration() {
  const fromProject = Number(state && state.project && state.project.durationMs || 0);
  const fromClients = Math.max(0, ...(state && state.clients || []).map(c => Number(c.durationMs || 0)));
  return Math.max(fromProject, fromClients);
}
function setStartPosition(value) {
  const max = projectDuration();
  const n = Math.max(0, Math.min(max, Number(value || 0)));
  document.getElementById("startPositionMs").value = String(Math.round(n));
  document.getElementById("seekPosition").value = String(Math.round(n));
}
function syncSeekControls() {
  const max = projectDuration();
  const range = document.getElementById("seekPosition");
  const input = document.getElementById("startPositionMs");
  range.max = String(Math.max(0, Math.round(max)));
  input.max = String(Math.max(0, Math.round(max)));
  if (document.activeElement !== range && document.activeElement !== input) {
    setStartPosition(input.value);
  }
}
function updateRoomStatus() {
  const roomState = state ? state.roomState : "EMPTY";
  document.getElementById("roomState").textContent = roomState || "EMPTY";
  const startAt = Number(state && state.scheduledStartAtServerTimeMs || 0);
  const now = Number(state && state.serverTimeMs || 0);
  if (startAt > now) {
    document.getElementById("countdown").textContent = ` starts in ${((startAt - now) / 1000).toFixed(1)}s`;
  } else if (startAt > 0) {
    document.getElementById("countdown").textContent = " start time reached";
  } else {
    document.getElementById("countdown").textContent = "";
  }
}
function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(reader.error || new Error("file read failed"));
    reader.readAsText(file, "utf-8");
  });
}
function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const bytes = new Uint8Array(reader.result || new ArrayBuffer(0));
      let binary = "";
      const chunkSize = 0x8000;
      for (let i = 0; i < bytes.length; i += chunkSize) {
        binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunkSize));
      }
      resolve(btoa(binary));
    };
    reader.onerror = () => reject(reader.error || new Error("file read failed"));
    reader.readAsArrayBuffer(file);
  });
}
function getPlaybackProfile() {
  return {
    speedPercent: Number(document.getElementById("profileSpeed").value || 95),
    holdMinMs: Number(document.getElementById("profileHoldMin").value || 150),
    sameKeyMinGapMs: Number(document.getElementById("profileSameKeyGap").value || 110),
    tapPressMs: Number(document.getElementById("profileTapPress").value || 14),
    longNoteReleaseEarlyMs: Number(document.getElementById("profileReleaseEarly").value || 80)
  };
}
async function api(path, body) {
  const res = await fetch(path, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body || {})});
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}
function loadSample() { document.getElementById("projectJson").value = JSON.stringify(sample, null, 2); }
async function loadProjectFile() {
  try {
    const file = document.getElementById("projectFile").files[0];
    if (!file) throw new Error("choose a project JSON file");
    document.getElementById("projectJson").value = await readFileAsText(file);
    setStatus(`loaded ${file.name}`);
  } catch (err) {
    setStatus(`error: ${err.message}`);
  }
}
async function uploadProject() {
  try {
    await api("/api/project", JSON.parse(document.getElementById("projectJson").value));
    setStatus("project uploaded");
    await refresh();
  } catch (err) {
    setStatus(`error: ${err.message}`);
  }
}
async function downloadCurrentProject() {
  try {
    const res = await fetch("/api/project/current");
    if (!res.ok) throw new Error(await res.text());
    const project = await res.json();
    const blob = new Blob([JSON.stringify(project, null, 2)], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${project.songId || "domiso_orchestra"}.project.json`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    setStatus("project downloaded");
  } catch (err) {
    setStatus(`error: ${err.message}`);
  }
}
async function importDomisoFiles() {
  try {
    const files = Array.from(document.getElementById("domisoFiles").files || []);
    if (!files.length) throw new Error("choose one or more txt/dms files");
    const tracks = [];
    for (let i = 0; i < files.length; i += 1) {
      const baseName = files[i].name.replace(/\.txt$/i, "");
      tracks.push({
        id: `track_${i + 1}`,
        name: baseName.replace(/\.dms$/i, "") || `track_${i + 1}`,
        fileName: files[i].name,
        contentBase64: await readFileAsBase64(files[i])
      });
    }
    const project = await api("/api/project/domiso", {
      songId: document.getElementById("domisoSongId").value || "domiso_project",
      title: document.getElementById("domisoTitle").value || "Domiso Project",
      layout: document.getElementById("domisoLayout").value,
      pitchNaming: document.getElementById("domisoPitchNaming").value,
      playbackProfile: getPlaybackProfile(),
      tracks,
    });
    setStatus(`imported ${project.project.tracks} txt/dms tracks`);
    await refresh();
  } catch (err) {
    setStatus(`error: ${err.message}`);
  }
}
async function importMidiFile() {
  try {
    const file = document.getElementById("midiFile").files[0];
    if (!file) throw new Error("choose a midi file");
    const project = await api("/api/project/midi", {
      songId: document.getElementById("midiSongId").value || "midi_project",
      title: document.getElementById("midiTitle").value || "MIDI Project",
      layout: document.getElementById("midiLayout").value,
      playbackProfile: getPlaybackProfile(),
      fileName: file.name,
      contentBase64: await readFileAsBase64(file)
    });
    setStatus(`imported ${project.project.tracks} midi tracks`);
    await refresh();
  } catch (err) {
    setStatus(`error: ${err.message}`);
  }
}
async function assign(trackId, clientId) { await api("/api/assign", {trackId, clientId}); await refresh(); }
async function setDelay(clientId, value) { await api("/api/client/" + encodeURIComponent(clientId) + "/delay", {inputDelayOffsetMs: Number(value)}); await refresh(); }
async function ready(clientId) { await api("/api/client/" + encodeURIComponent(clientId) + "/ready", {}); await refresh(); }
async function testPulse(clientId) { await api("/api/client/" + encodeURIComponent(clientId) + "/test", {keys: ["y"], count: 3, intervalMs: 500}); await refresh(); }
async function prepare() { await api("/api/prepare", {}); setStatus("prepare sent"); await refresh(); }
async function start() {
  const startPositionMs = Number(document.getElementById("startPositionMs").value || 0);
  const result = await api("/api/start", {delayMs: 5000, startPositionMs});
  setStartPosition(result.startPositionMs || 0);
  setStatus("start scheduled");
  await refresh();
}
async function startFromBeginning() { setStartPosition(0); await start(); }
function useCurrentProgress() {
  const clients = state && state.clients || [];
  const progress = Math.max(0, ...clients.map(c => Number(c.progressMs || 0)));
  setStartPosition(progress);
}
async function pause() { await api("/api/pause", {}); setStatus("pause sent"); await refresh(); }
async function resume() { await api("/api/resume", {}); setStatus("resume sent"); await refresh(); }
async function stop() { await api("/api/stop", {}); setStatus("stop sent"); await refresh(); }
async function refresh() {
  state = await (await fetch("/api/state")).json();
  updateRoomStatus();
  syncSeekControls();
  const clients = state.clients || [];
  document.getElementById("clients").innerHTML = clients.map(c => `
    <tr>
      <td>${esc(c.client_id)}</td><td>${esc(c.name)}</td><td class="state">${esc(c.state)}</td><td>${esc(c.layout)}</td><td>${esc(c.windowTitle || "")}</td>
      <td><input type="number" value="${Number(c.input_delay_offset_ms || 0)}" data-delay-client="${esc(c.client_id)}" style="width:80px"></td>
      <td>${fmtNumber(c.syncRttMs)} ms<br><span class="small">best ${fmtNumber(c.bestSyncRttMs)} ms</span></td>
      <td>${fmtNumber(c.clockOffsetMs)} ms</td>
      <td><progress max="${Math.max(1, Number(c.durationMs || 0))}" value="${Math.max(0, Number(c.progressMs || 0))}"></progress><br><span class="small">${progressText(c)}</span></td>
      <td>${esc((c.loaded_tracks || []).join(", "))}</td>
      <td><button data-ready-client="${esc(c.client_id)}">Ready</button><button data-test-client="${esc(c.client_id)}">Pulse</button></td>
      <td class="error">${esc(c.error || "")}</td>
    </tr>`).join("");
  const tracks = state.project ? state.project.tracks : [];
  function options(selected) {
    let html = `<option value="" ${selected ? "" : "selected"}>-</option>`;
    for (const client of clients) {
      const id = String(client.client_id);
      html += `<option value="${esc(id)}" ${id === selected ? "selected" : ""}>${esc(id)}</option>`;
    }
    return html;
  }
  document.getElementById("tracks").innerHTML = tracks.map(t => `
    <tr><td>${esc(t.id)}<br><span class="small">${esc(t.name)}</span></td><td>${Number(t.events || 0)}<br><span class="small">${(Number(t.durationMs || 0) / 1000).toFixed(1)} s</span></td>
    <td><select data-track="${esc(t.id)}">${options(String(t.assignedTo || ""))}</select></td></tr>`).join("");
  document.querySelectorAll("[data-delay-client]").forEach(input => {
    input.onchange = () => setDelay(input.dataset.delayClient, input.value);
  });
  document.querySelectorAll("[data-ready-client]").forEach(button => {
    button.onclick = () => ready(button.dataset.readyClient);
  });
  document.querySelectorAll("[data-test-client]").forEach(button => {
    button.onclick = () => testPulse(button.dataset.testClient);
  });
  document.querySelectorAll("select[data-track]").forEach(select => {
    select.onchange = () => assign(select.dataset.track, select.value);
  });
}
document.getElementById("startPositionMs").addEventListener("input", event => setStartPosition(event.target.value));
document.addEventListener("keydown", event => {
  const tag = String(event.target && event.target.tagName || "").toUpperCase();
  if (["INPUT", "TEXTAREA", "SELECT"].includes(tag)) return;
  if (event.key === "F7") { event.preventDefault(); pause(); }
  if (event.key === "F8") { event.preventDefault(); stop(); }
  if (event.key === "F9") { event.preventDefault(); startFromBeginning(); }
  if (event.key === "F10") { event.preventDefault(); resume(); }
});
loadSample();
setInterval(refresh, 1000);
refresh();
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return INDEX_HTML


@app.get("/api/state")
async def state() -> Dict[str, object]:
    return await room.public_state()


@app.get("/api/project/current")
async def current_project() -> JSONResponse:
    async with room.lock:
        if not room.project:
            raise HTTPException(404, "no project loaded")
        return JSONResponse(room.project)


@app.post("/api/project")
async def set_project(payload: Dict[str, object]) -> Dict[str, object]:
    try:
        project = normalize_project(payload)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    async with room.lock:
        room.project = project
        room.assignments = {}
        room.room_state = "PROJECT_LOADED"
        room.scheduled_start_at_ms = None
        room.scheduled_start_position_ms = 0
        for session in room.clients.values():
            session.loaded_tracks = []
            session.progress_ms = 0
            session.duration_ms = 0
            if session.websocket is not None and session.state not in {"DISCONNECTED", "ERROR"}:
                session.state = "CONNECTED"
    return {"ok": True, "project": {"songId": project["songId"], "tracks": len(project["tracks"])}}


@app.post("/api/project/domiso")
async def set_project_from_domiso(payload: Dict[str, object]) -> Dict[str, object]:
    try:
        project = project_from_domiso_tracks(
            song_id=str(payload.get("songId") or "domiso_project"),
            title=str(payload.get("title") or payload.get("songId") or "Domiso Project"),
            tracks=payload.get("tracks") or [],
            default_layout=str(payload.get("layout") or "sky15"),
            pitch_naming=str(payload.get("pitchNaming") or "standard"),
            playback_profile=payload.get("playbackProfile") if isinstance(payload.get("playbackProfile"), dict) else None,
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    async with room.lock:
        room.project = project
        room.assignments = {}
        room.room_state = "PROJECT_LOADED"
        room.scheduled_start_at_ms = None
        room.scheduled_start_position_ms = 0
        for session in room.clients.values():
            session.loaded_tracks = []
            session.progress_ms = 0
            session.duration_ms = 0
            if session.websocket is not None and session.state not in {"DISCONNECTED", "ERROR"}:
                session.state = "CONNECTED"
    return {"ok": True, "project": {"songId": project["songId"], "tracks": len(project["tracks"])}}


@app.post("/api/project/midi")
async def set_project_from_midi(payload: Dict[str, object]) -> Dict[str, object]:
    try:
        content_base64 = str(payload.get("contentBase64") or "")
        if not content_base64:
            raise ValueError("contentBase64 is required")
        project = midi_base64_to_project(
            content_base64=content_base64,
            song_id=str(payload.get("songId") or "midi_project"),
            title=str(payload.get("title") or payload.get("songId") or payload.get("fileName") or "MIDI Project"),
            layout=str(payload.get("layout") or "domiso36"),
            playback_profile=payload.get("playbackProfile") if isinstance(payload.get("playbackProfile"), dict) else None,
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    async with room.lock:
        room.project = project
        room.assignments = {}
        room.room_state = "PROJECT_LOADED"
        room.scheduled_start_at_ms = None
        room.scheduled_start_position_ms = 0
        for session in room.clients.values():
            session.loaded_tracks = []
            session.progress_ms = 0
            session.duration_ms = 0
            if session.websocket is not None and session.state not in {"DISCONNECTED", "ERROR"}:
                session.state = "CONNECTED"
    return {"ok": True, "project": {"songId": project["songId"], "tracks": len(project["tracks"])}}


@app.post("/api/assign")
async def assign(payload: Dict[str, object]) -> Dict[str, object]:
    track_id = str(payload.get("trackId") or "")
    client_id = str(payload.get("clientId") or "")
    async with room.lock:
        if not room.project:
            raise HTTPException(400, "no project loaded")
        track_ids = {str(t.get("id")) for t in room.project.get("tracks", []) if isinstance(t, dict)}
        if track_id not in track_ids:
            raise HTTPException(404, f"unknown track: {track_id}")
        if client_id:
            if client_id not in room.clients:
                raise HTTPException(404, f"unknown client: {client_id}")
            room.assignments[track_id] = client_id
        else:
            room.assignments.pop(track_id, None)
    return {"ok": True}


@app.post("/api/client/{client_id}/delay")
async def set_client_delay(client_id: str, payload: Dict[str, object]) -> Dict[str, object]:
    delay = int(payload.get("inputDelayOffsetMs") or 0)
    async with room.lock:
        session = room.clients.get(client_id)
        if not session:
            raise HTTPException(404, f"unknown client: {client_id}")
        session.input_delay_offset_ms = delay
    try:
        await room.send_command(client_id, {"type": "SET_DELAY", "inputDelayOffsetMs": delay})
    except RuntimeError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {"ok": True, "clientId": client_id, "inputDelayOffsetMs": delay}


@app.post("/api/client/{client_id}/ready")
async def set_client_ready(client_id: str) -> Dict[str, object]:
    async with room.lock:
        session = room.clients.get(client_id)
        if not session:
            raise HTTPException(404, f"unknown client: {client_id}")
        if session.websocket is None:
            raise HTTPException(409, f"client not connected: {client_id}")
    try:
        await room.send_command(client_id, {"type": "SET_READY"})
    except RuntimeError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {"ok": True, "clientId": client_id}


@app.post("/api/client/{client_id}/test")
async def test_client(client_id: str, payload: Dict[str, object]) -> Dict[str, object]:
    keys = payload.get("keys") or ["y"]
    if not isinstance(keys, list) or not keys:
        raise HTTPException(400, "keys must be a non-empty list")
    command = {
        "type": "TEST_PULSE",
        "keys": [str(k) for k in keys],
        "count": max(1, min(8, int(payload.get("count") or 3))),
        "intervalMs": max(100, min(3000, int(payload.get("intervalMs") or 500))),
        "pressMs": max(10, min(500, int(payload.get("pressMs") or 80))),
    }
    try:
        await room.send_command(client_id, command)
    except RuntimeError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {"ok": True, "clientId": client_id}


@app.post("/api/prepare")
async def prepare() -> Dict[str, object]:
    async with room.lock:
        if not room.project:
            raise HTTPException(400, "no project loaded")
        assignments = dict(room.assignments)
        project = room.project
    grouped: Dict[str, List[str]] = {}
    for track_id, client_id in assignments.items():
        grouped.setdefault(client_id, []).append(track_id)
    if not grouped:
        raise HTTPException(400, "no tracks assigned")
    sent = []
    for client_id, track_ids in grouped.items():
        command = {
            "type": "LOAD_PROJECT",
            "project": subset_project(project, track_ids),
            "assignedTrackIds": track_ids,
        }
        try:
            await room.send_command(client_id, command)
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc
        sent.append({"clientId": client_id, "tracks": track_ids})
    async with room.lock:
        room.room_state = "LOADING"
        room.scheduled_start_at_ms = None
        room.scheduled_start_position_ms = 0
    return {"ok": True, "sent": sent}


@app.post("/api/start")
async def start(payload: Dict[str, object]) -> Dict[str, object]:
    delay_ms = int(payload.get("delayMs") or 5000)
    requested_position_ms = int(payload.get("startPositionMs") or 0)
    force = bool(payload.get("force") or False)
    client_ids = await room.assigned_client_ids()
    if not client_ids:
        raise HTTPException(400, "no assigned clients")
    async with room.lock:
        project = room.project
        not_ready = [
            cid
            for cid in client_ids
            if not room.clients.get(cid) or room.clients[cid].state not in {"READY", "ARMED", "FINISHED"}
        ]
    duration_ms = playback_duration_ms(project) if project else 0
    start_position_ms = max(0, min(duration_ms, requested_position_ms))
    if not_ready and not force:
        raise HTTPException(409, f"clients not ready: {', '.join(not_ready)}")
    start_at = server_time_ms() + delay_ms
    for client_id in client_ids:
        async with room.lock:
            song_id = room.project.get("songId") if room.project else ""
        try:
            await room.send_command(
                client_id,
                {
                    "type": "START",
                    "songId": song_id,
                    "startAtServerTimeMs": start_at,
                    "startPositionMs": start_position_ms,
                },
            )
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc
    async with room.lock:
        room.room_state = "ARMED"
        room.scheduled_start_at_ms = start_at
        room.scheduled_start_position_ms = start_position_ms
    return {
        "ok": True,
        "startAtServerTimeMs": start_at,
        "startPositionMs": start_position_ms,
        "durationMs": duration_ms,
        "clients": client_ids,
    }


@app.post("/api/stop")
async def stop() -> Dict[str, object]:
    client_ids = await room.assigned_client_ids()
    for client_id in client_ids:
        try:
            await room.send_command(client_id, {"type": "STOP"})
        except RuntimeError:
            pass
    async with room.lock:
        room.room_state = "STOPPED"
        room.scheduled_start_at_ms = None
        room.scheduled_start_position_ms = 0
    return {"ok": True, "clients": client_ids}


@app.post("/api/pause")
async def pause() -> Dict[str, object]:
    client_ids = await room.assigned_client_ids()
    if not client_ids:
        raise HTTPException(400, "no assigned clients")
    for client_id in client_ids:
        try:
            await room.send_command(client_id, {"type": "PAUSE"})
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc
    async with room.lock:
        room.room_state = "PAUSED"
    return {"ok": True, "clients": client_ids}


@app.post("/api/resume")
async def resume() -> Dict[str, object]:
    client_ids = await room.assigned_client_ids()
    if not client_ids:
        raise HTTPException(400, "no assigned clients")
    for client_id in client_ids:
        try:
            await room.send_command(client_id, {"type": "RESUME"})
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc
    async with room.lock:
        room.room_state = "PLAYING"
        room.scheduled_start_at_ms = None
        room.scheduled_start_position_ms = 0
    return {"ok": True, "clients": client_ids}


@app.websocket("/ws/player")
async def player_socket(ws: WebSocket) -> None:
    await ws.accept()
    client_id = ""
    try:
        hello = await ws.receive_json()
        if hello.get("type") != "HELLO":
            await ws.send_json({"type": "ERROR", "error": "first message must be HELLO"})
            return
        session = await room.register(ws, hello)
        client_id = session.client_id
        await ws.send_json({"type": "WELCOME", "serverTimeMs": server_time_ms()})
        while True:
            msg = await ws.receive_json()
            msg_type = msg.get("type")
            if msg_type == "SYNC_REQUEST":
                await ws.send_json(
                    {
                        "type": "SYNC_ACK",
                        "clientSentMonotonicMs": msg.get("clientSentMonotonicMs"),
                        "serverTimeMs": server_time_ms(),
                    }
                )
            elif msg_type == "STATE":
                await room.update_client(client_id, msg)
            else:
                await room.update_client(client_id, {})
    except WebSocketDisconnect:
        pass
    finally:
        if client_id:
            await room.disconnect(client_id, ws)


def main() -> None:
    import argparse
    import uvicorn

    ap = argparse.ArgumentParser(description="Run the Domiso Orchestra Conductor LAN server.")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    uvicorn.run("domiso_orchestra.conductor:app", host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()
