from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlatformConfig:
    environment: str = os.getenv("APEX_ENV", "local")
    lakehouse_root: Path = Path(os.getenv("APEX_LAKEHOUSE_ROOT", "data/lakehouse"))
    vector_store_path: Path = Path(
        os.getenv("VECTOR_STORE_PATH", "data/vector_store/governed_gold_index.json")
    )
    audit_log_path: Path = Path(os.getenv("AUDIT_LOG_PATH", "data/sample/audit_events.jsonl"))
    prompt_version: str = os.getenv("PROMPT_VERSION", "amip-reporting-v1.3")


def get_config() -> PlatformConfig:
    return PlatformConfig()

