from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def validate_checkpoint(checkpoint_dir: Path) -> dict:
    offsets = sorted(checkpoint_dir.glob("offsets/*.json"))
    commits = sorted(checkpoint_dir.glob("commits/*.json"))
    status = "healthy" if offsets and commits else "missing_checkpoint_files"
    return {
        "checkpoint_dir": str(checkpoint_dir),
        "status": status,
        "offset_files": len(offsets),
        "commit_files": len(commits),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    result = validate_checkpoint(Path("data/lakehouse/bronze/card_transactions/_checkpoints"))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

