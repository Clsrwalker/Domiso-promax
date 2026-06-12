from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, Iterable, List

from .domiso_parser import note_events_to_track
from .domiso_sheet import sheet_text_from_base64, split_published_text
from .playback import PlaybackProfile


def normalize_project(payload: Dict[str, object]) -> Dict[str, object]:
    song_id = str(payload.get("songId") or payload.get("id") or f"song_{int(time.time())}")
    title = str(payload.get("title") or song_id)
    tracks_in = payload.get("tracks") or []
    if not isinstance(tracks_in, list):
        raise ValueError("project.tracks must be a list")
    tracks: List[Dict[str, object]] = []
    for index, raw in enumerate(tracks_in, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"track {index} must be an object")
        track_id = str(raw.get("id") or f"track_{index}")
        events = raw.get("events") or []
        if not isinstance(events, list):
            raise ValueError(f"track {track_id}.events must be a list")
        normalized_events = []
        for ev_index, event in enumerate(events, start=1):
            if not isinstance(event, dict):
                raise ValueError(f"track {track_id} event {ev_index} must be an object")
            keys = event.get("keys") or []
            if not isinstance(keys, list):
                raise ValueError(f"track {track_id} event {ev_index}.keys must be a list")
            normalized_events.append(
                {
                    "timeMs": int(round(float(event.get("timeMs", 0)))),
                    "durationMs": max(1, int(round(float(event.get("durationMs", event.get("lengthMs", 80)))))),
                    "keys": [str(k) for k in keys],
                    **({"midiNotes": event["midiNotes"]} if "midiNotes" in event else {}),
                }
            )
        normalized_events.sort(key=lambda e: (e["timeMs"], ",".join(e["keys"])))
        tracks.append(
            {
                "id": track_id,
                "name": str(raw.get("name") or track_id),
                "layout": str(raw.get("layout") or payload.get("layout") or "sky15"),
                "events": normalized_events,
                **({"source": raw["source"]} if "source" in raw else {}),
                **({"stats": raw["stats"]} if "stats" in raw else {}),
            }
        )
    return {
        "schemaVersion": "domiso-orchestra.project.v1",
        "songId": song_id,
        "title": title,
        "createdAt": payload.get("createdAt") or time.strftime("%Y-%m-%d %H:%M:%S"),
        "playbackProfile": PlaybackProfile.from_payload(payload.get("playbackProfile")).to_dict(),
        "tracks": tracks,
        "meta": payload.get("meta") or {},
    }


def load_project(path: str | Path) -> Dict[str, object]:
    return normalize_project(json.loads(Path(path).read_text(encoding="utf-8")))


def save_project(project: Dict[str, object], path: str | Path) -> None:
    Path(path).write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")


def project_from_domiso_tracks(
    *,
    song_id: str,
    title: str,
    tracks: Iterable[Dict[str, object]],
    default_layout: str = "sky15",
    pitch_naming: str = "standard",
    playback_profile: Dict[str, object] | None = None,
) -> Dict[str, object]:
    converted = []
    for index, item in enumerate(tracks, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"track {index} must be an object")
        source_extra: Dict[str, object] = {}
        if item.get("contentBase64"):
            text, source_extra = sheet_text_from_base64(str(item["contentBase64"]))
        else:
            raw_text = str(item.get("text") or "")
            _, text = split_published_text(raw_text)
        if not text.strip():
            raise ValueError(f"track {index} has empty text")
        track_id = str(item.get("id") or f"track_{index}")
        converted_track = note_events_to_track(
            track_id=track_id,
            name=str(item.get("name") or track_id),
            text=text,
            layout=str(item.get("layout") or default_layout),
            pitch_naming=str(item.get("pitchNaming") or pitch_naming),
        )
        if isinstance(item.get("source"), dict):
            converted_track["source"] = {**converted_track.get("source", {}), **item["source"]}
        if source_extra:
            converted_track["source"] = {**converted_track.get("source", {}), **source_extra}
        if item.get("fileName"):
            converted_track["source"] = {**converted_track.get("source", {}), "fileName": str(item["fileName"])}
        converted.append(converted_track)
    return normalize_project(
        {
            "songId": song_id,
            "title": title,
            "playbackProfile": playback_profile or PlaybackProfile().to_dict(),
            "tracks": converted,
        }
    )


def subset_project(project: Dict[str, object], track_ids: Iterable[str]) -> Dict[str, object]:
    wanted = set(track_ids)
    return {
        **project,
        "tracks": [t for t in project.get("tracks", []) if isinstance(t, dict) and str(t.get("id")) in wanted],
    }
