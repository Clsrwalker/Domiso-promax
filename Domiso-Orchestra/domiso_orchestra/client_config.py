from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def default_config_path(client_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in client_id).strip("_") or "client"
    return Path.home() / ".domiso-orchestra" / f"{safe}.json"


def load_client_config(path: str | Path | None) -> Dict[str, object]:
    if not path:
        return {}
    config_path = Path(path)
    if not config_path.exists():
        return {}
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"client config must be a JSON object: {config_path}")
    return data


def save_client_config(path: str | Path, data: Dict[str, object]) -> None:
    config_path = Path(path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
