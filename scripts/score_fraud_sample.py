from __future__ import annotations

import csv
import json
from pathlib import Path

from apex_meridian.ml.fraud_model import FraudAnomalyScorer


def main() -> None:
    input_files = sorted(Path("data/generated").glob("**/transactions/*.csv"))
    scorer = FraudAnomalyScorer()
    scored = []
    for path in input_files[:1]:
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                result = scorer.score(row)
                scored.append(result.__dict__)
                if len(scored) >= 1000:
                    break
    output = Path("data/sample/fraud_scores.json")
    output.write_text(json.dumps({"scores": scored}, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()

