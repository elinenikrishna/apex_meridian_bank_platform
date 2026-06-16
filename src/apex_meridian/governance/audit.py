from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class AuditLogger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, actor: str, action: str, dataset: str, status: str, metadata: dict | None = None) -> dict:
        event = {
            "event_id": f"audit-{uuid4().hex[:12]}",
            "actor": actor,
            "action": action,
            "dataset": dataset,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")
        return event

