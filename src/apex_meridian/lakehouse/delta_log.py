from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def write_delta_commit(
    table_path: Path,
    operation: str,
    files: list[str],
    metrics: dict | None = None,
) -> Path:
    log_dir = table_path / "_delta_log"
    log_dir.mkdir(parents=True, exist_ok=True)
    version = len(list(log_dir.glob("*.json")))
    commit_path = log_dir / f"{version:020d}.json"
    commit = {
        "commitInfo": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": operation,
            "engine": "apex-meridian-local-delta-emulator",
            "operationMetrics": metrics or {},
        },
        "add": [{"path": file_path, "dataChange": True} for file_path in files],
    }
    with commit_path.open("w", encoding="utf-8") as handle:
        json.dump(commit, handle, indent=2)
    return commit_path

