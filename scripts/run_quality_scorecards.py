from __future__ import annotations

import json
from pathlib import Path

from apex_meridian.governance.quality import evaluate_csv


def main() -> None:
    candidates = sorted(Path("data/generated").glob("**/transactions/*.csv"))
    results = [evaluate_csv(path, limit=10000) for path in candidates[:5]]
    output = Path("data/sample/data_quality_scorecards.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"scorecards": results}, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()

